import graphene
from graphql_jwt import relay


class AuthMutation(graphene.ObjectType):
    token_auth = relay.ObtainJSONWebToken.Field()
    verify_token = relay.Verify.Field()
    refresh_token = relay.Refresh.Field()
    revoke_token = relay.Revoke.Field()
