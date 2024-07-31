import django_filters
import graphene
from graphene import relay
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from evidenta.core.user.models import Role


class RoleFilter(django_filters.FilterSet):
    order_by = django_filters.OrderingFilter(
        ("name", "name"),
    )

    name = django_filters.CharFilter(field_name="name", lookup_expr="iexact")
    name_contains = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    name_startswith = django_filters.CharFilter(field_name="name", lookup_expr="istartswith")

    class Meta:
        model = Role
        fields = {
            "name": ["iexact", "icontains", "istartswith"],
        }


class RoleType(DjangoObjectType):
    class Meta:
        model = Role
        interfaces = (relay.Node,)
        fields = "__all__"


class RoleQuery(graphene.ObjectType):
    all_roles = DjangoFilterConnectionField(RoleType, filterset_class=RoleFilter)
    role = graphene.relay.Node.Field(RoleType)
