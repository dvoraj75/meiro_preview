from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

import graphene
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_relay import to_global_id

from evidenta.common.enums import ApiErrorCode
from evidenta.common.exceptions import (
    GraphqlApiException,
    InvalidFieldValueException,
    ObjectDoesNotExist,
    ObjectDoesNotExistAPIException,
    UnexpectedApiError,
)
from evidenta.common.utils.auth import login_required, permissions_required
from evidenta.core.user.service import UserService


class UserNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
        filter_fields = {
            "first_name": ["exact", "icontains", "istartswith"],
            "last_name": ["exact", "icontains", "istartswith"],
            "email": ["exact", "icontains", "istartswith"],
            "username": ["exact", "icontains", "istartswith"],
            "role": ["exact"],
            "phone_number": ["exact", "icontains"],
            "gender": ["exact"],
            "companies": ["exact", "icontains"],
        }
        exclude = ["password", "is_superuser"]
        interfaces = (graphene.relay.Node,)

    pk = graphene.Int()

    @classmethod
    @login_required
    @permissions_required(["api.view_user"])
    def get_queryset(cls, _, info):
        try:
            return UserService().get_all(as_user=info.context.user)
        except Exception as e:
            raise UnexpectedApiError(
                message=str(e),
                error_data={
                    "method": "get_queryset",
                    "input_data": {},
                    "as_user": info.context.user.username,
                },
                error_code=ApiErrorCode.UNEXPECTED_ERROR,
            ) from e

    @classmethod
    @login_required
    @permissions_required(["api.view_user"])
    def get_user(cls, user_id, info):
        try:
            return UserService().get(user_id=user_id, as_user=info.context.user)
        except ObjectDoesNotExist as e:
            global_id = to_global_id("UserNode", user_id)
            raise ObjectDoesNotExistAPIException(
                message=f"User with global id: {global_id} does not exist",
                error_data={"id": user_id, "global_id": global_id},
                error_code=ApiErrorCode.OBJECT_NOT_FOUND,
            ) from e
        except Exception as e:
            raise UnexpectedApiError(
                message=str(e),
                error_data={
                    "method": "get_user",
                    "input_data": {"user_id": user_id},
                    "as_user": info.context.user.username,
                },
                error_code=ApiErrorCode.UNEXPECTED_ERROR,
            ) from e

    @classmethod
    def get_node(cls, info, id):
        return cls.get_user(id, info)


class UserQuery(graphene.ObjectType):
    user = graphene.relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)


class MeQuery(graphene.ObjectType):
    me = graphene.Field(UserNode)

    @classmethod
    @login_required
    def resolve_me(cls, _, info):
        return info.context.user


class CreateUser(graphene.relay.ClientIDMutation):
    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        title = graphene.String()
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        role = graphene.Int(required=True)
        phone_number = graphene.String()
        gender = graphene.Int()
        birthday = graphene.Date()
        companies = graphene.List(graphene.ID)

    user = graphene.Field(UserNode)

    @classmethod
    @login_required
    @permissions_required(["api.add_user"])
    def mutate_and_get_payload(cls, root, info, **kwargs):
        if kwargs.get("companies") and not info.context.user.has_perm("api.assign_company_user"):
            raise PermissionDenied("Permission denied: Can't assign companies to user")
        try:
            return CreateUser(user=UserService().create(**kwargs))
        except (InvalidFieldValueException, Exception) as e:
            raise GraphqlApiException(e) from e


class UpdateUser(graphene.relay.ClientIDMutation):
    class Input:
        user_id = graphene.ID(required=True)
        username = graphene.String()
        password = graphene.String()
        title = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        role = graphene.Int()
        phone_number = graphene.String()
        gender = graphene.Int()
        birthday = graphene.Date()
        companies = graphene.List(graphene.ID)

    @classmethod
    @login_required
    @permissions_required(["api.change_user"])
    def mutate_and_get_payload(cls, root, info, user_id, **kwargs):
        if kwargs.get("companies") and not info.context.user.has_perm("api.assign_company_user"):
            raise PermissionDenied("Permission denied: Can't assign companies to user")

        try:
            UserService().update(user_id=user_id, as_user=info.context.user, **kwargs)
        except (InvalidFieldValueException, Exception) as e:
            raise GraphqlApiException(e) from e
        return UpdateUser()


class DeleteUser(graphene.relay.ClientIDMutation):
    class Input:
        user_id = graphene.ID()

    @classmethod
    @login_required
    @permissions_required(["api.delete_user"])
    def mutate_and_get_payload(cls, root, info, user_id):
        try:
            UserService().delete(user_id=user_id, as_user=info.context.user)
        except (InvalidFieldValueException, Exception) as e:
            raise GraphqlApiException(e) from e
        return DeleteUser()


class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
