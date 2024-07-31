from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError

import graphene
from graphene_django import DjangoObjectType
from graphql_jwt import relay

from evidenta.common.enums import ApiErrorCode
from evidenta.common.schemas.utils import (
    InvalidDataAPIException,
    get_error_message_from_error_code,
    login_required,
    raise_does_not_exist_error,
    raise_invalid_token_exception,
    raise_unexpected_error,
    raise_validation_error,
)
from evidenta.core.auth.exceptions import InvalidTokenError
from evidenta.core.auth.models import Token
from evidenta.core.user.service import UserService


class TokenType(DjangoObjectType):
    class Meta:
        model = Token
        fields = "__all__"


class SendInvitationLink(graphene.relay.ClientIDMutation):
    class Input:
        email = graphene.String(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, _, info, email):
        try:
            UserService().invite_user_by_email(as_user=info.context.user, email=email)
        except ObjectDoesNotExist as e:
            raise_does_not_exist_error("User", {"field": "email", "value": email}, e)
        except Exception as e:
            raise_unexpected_error(
                method="UserService:invite_user_by_email",
                input_data={"email": email, "as_user": info.context.user.pk},
                user=info.context.user,
                original_error=e,
            )
        return SendInvitationLink()


class SetPassword(graphene.relay.ClientIDMutation):
    class Input:
        token = graphene.String(required=True)
        password = graphene.String(required=True)
        password_confirm = graphene.String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, _, info, token, password, password_confirm):
        if password != password_confirm:
            raise InvalidDataAPIException(
                message=get_error_message_from_error_code(ApiErrorCode.INVALID_PASSWORDS),
                error_code=ApiErrorCode.INVALID_PASSWORDS,
            )

        try:
            UserService().set_password_to_user_by_token(token, password)
        except ObjectDoesNotExist as e:
            raise_does_not_exist_error("Token", {"field": "token", "value": token}, e)
        except InvalidTokenError as e:
            raise_invalid_token_exception(e)
        except ValidationError as e:
            raise_validation_error(e, obj_name="User")
        except Exception as e:
            raise_unexpected_error(
                method="UserService:set_password_to_user_by_token",
                input_data={"token": token, "password": password},
                user=info.context.user,
                original_error=e,
            )
        return SetPassword()


class SendChangePasswordOTPToken(graphene.relay.ClientIDMutation):
    class Input:
        email = graphene.String(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, _, info, email):
        try:
            UserService().request_password_change(email=email, as_user=info.context.user)
        except ObjectDoesNotExist as e:
            raise_does_not_exist_error("User", {"field": "email", "value": email}, e)
        except Exception as e:
            raise_unexpected_error(
                method="UserService:request_password_change",
                input_data={"email": email, "as_user": info.context.user.pk},
                user=info.context.user,
                original_error=e,
            )
        return SendChangePasswordOTPToken()


class ChangePassword(graphene.relay.ClientIDMutation):
    class Input:
        old_password = graphene.String(required=True)
        new_password = graphene.String(required=True)
        new_password_confirm = graphene.String(required=True)
        token = graphene.String(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, _, info, old_password, new_password, new_password_confirm, token):
        if not check_password(old_password, info.context.user.password):
            raise InvalidDataAPIException(
                message=get_error_message_from_error_code(ApiErrorCode.INVALID_OLD_PASSWORD),
                error_code=ApiErrorCode.INVALID_OLD_PASSWORD,
            )

        if new_password != new_password_confirm:
            raise InvalidDataAPIException(
                message=get_error_message_from_error_code(ApiErrorCode.INVALID_PASSWORDS),
                error_code=ApiErrorCode.INVALID_PASSWORDS,
            )

        try:
            UserService().change_user_password_by_token(token, new_password, info.context.user)
        except ObjectDoesNotExist as e:
            raise_does_not_exist_error("Token", {"field": "token", "value": token}, e)
        except InvalidTokenError as e:
            raise_invalid_token_exception(e)
        except ValidationError as e:
            raise_validation_error(e, obj_name="User")
        except Exception as e:
            raise_unexpected_error(
                method="AuthService:set_user_password",
                input_data={"token": token, "new_password": new_password, "as_user": info.context.user.pk},
                user=info.context.user,
                original_error=e,
            )
        return ChangePassword()


class SendResetPasswordLink(graphene.relay.ClientIDMutation):
    class Input:
        email = graphene.String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, _, info, email):
        try:
            UserService().request_password_reset(email=email)
        except ObjectDoesNotExist:
            return SendInvitationLink()
        except Exception as e:
            raise_unexpected_error(
                method="UserService:request_password_reset",
                input_data={"email": email},
                user=info.context.user,
                original_error=e,
            )
        return SendInvitationLink()


class AuthMutation(graphene.ObjectType):
    token_auth = relay.ObtainJSONWebToken.Field()
    verify_token = relay.Verify.Field()
    refresh_token = relay.Refresh.Field()
    revoke_token = relay.Revoke.Field()

    send_invitation_link = SendInvitationLink.Field()
    set_password = SetPassword.Field()
    send_change_password_otp_token = SendChangePasswordOTPToken.Field()
    change_password = ChangePassword.Field()
    send_reset_password_link = SendResetPasswordLink.Field()
