import graphene

from evidenta.core.auth.schema import AuthMutation
from evidenta.core.user.schemas import MeQuery, RoleQuery, UserMutation, UserQuery


class Query(UserQuery, MeQuery, RoleQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, UserMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
