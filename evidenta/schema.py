import graphene

from evidenta.core.auth.schema import AuthMutation
from evidenta.core.user.schema import MeQuery, UserMutation, UserQuery


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, UserMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
