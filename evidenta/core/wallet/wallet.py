from django.contrib.auth.hashers import check_password

import graphene
from api.common.utils import login_required
from api.models.wallet import WalletRecord
from graphene import Node, relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError, GraphQLResolveInfo


class WalletRecordNode(DjangoObjectType):
    class Meta:
        model = WalletRecord
        fields = ("username", "description")
        filter_fields = ("id",)
        interfaces = (relay.Node,)

    decrypted_password = graphene.String()

    def resolve_decrypted_password(self: WalletRecord, info: GraphQLResolveInfo) -> str:
        """
        NOTE: `self` is typed as WalletRecord, because Graphene DjangoObjectType use `self`
        variable as `Meta.model` instance.
        """
        # pylint: disable=unused-argument
        return self.get_decrypted_password()


class WalletRecordsQuery(graphene.ObjectType):
    wallet_record = graphene.Field(WalletRecordNode)
    wallet_records = DjangoFilterConnectionField(WalletRecordNode, master_password=graphene.String(required=True))

    @classmethod
    @login_required
    def resolve_wallet_records(cls, _, info: GraphQLResolveInfo, master_password: str):
        wallet = info.context.user.wallet
        if not check_password(master_password, wallet.password):
            raise GraphQLError("Invalid wallet password!")
        return wallet.records.all()


class WalletRecordsCreate(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        description = graphene.String(required=True)

    wallet_record = graphene.Field(WalletRecordNode)

    @classmethod
    @login_required
    def mutate(
        cls, _, info: GraphQLResolveInfo, username: str, password: str, description: str
    ) -> "WalletRecordsCreate":
        wallet_record = WalletRecord.objects.create(
            wallet=info.context.user.wallet,
            username=username,
            password=password,
            description=description,
        )

        return WalletRecordsCreate(wallet_record=wallet_record)


class WalletRecordsUpdate(graphene.Mutation):
    class Arguments:
        record_id = graphene.ID(required=True)
        username = graphene.String()
        password = graphene.String()
        description = graphene.String()

    wallet_record = graphene.Field(WalletRecordNode)

    @classmethod
    @login_required
    def mutate(cls, _, info: GraphQLResolveInfo, record_id: str, **kwargs) -> "WalletRecordsUpdate":
        try:
            wallet_record: WalletRecord = Node.get_node_from_global_id(info, record_id)
        except Exception as exc:
            raise GraphQLError("Invalid record ID!") from exc
        if not wallet_record or wallet_record.wallet.user != info.context.user:
            raise GraphQLError("Non-existing wallet record!")
        for key, value in kwargs.items():
            if key == "password":
                wallet_record.set_new_password(value)
            else:
                setattr(wallet_record, key, value)
        wallet_record.save()
        return WalletRecordsUpdate(wallet_record=wallet_record)


class WalletRecordsDelete(graphene.Mutation):
    class Arguments:
        record_id = graphene.ID(required=True)

    wallet_record = graphene.Field(WalletRecordNode)

    @classmethod
    @login_required
    def mutate(cls, _, info: GraphQLResolveInfo, record_id: str) -> "WalletRecordsDelete":
        try:
            wallet_record: WalletRecord = Node.get_node_from_global_id(info, record_id)
        except Exception as exc:
            raise GraphQLError("Invalid record ID!") from exc
        if not wallet_record or wallet_record.wallet.user != info.context.user:
            raise GraphQLError("Non-existing wallet record!")
        wallet_record.delete()
        return WalletRecordsDelete(wallet_record=wallet_record)


class WalletRecordsMutation(graphene.ObjectType):
    create_wallet_record = WalletRecordsCreate.Field()
    update_wallet_record = WalletRecordsUpdate.Field()
    delete_wallet_record = WalletRecordsDelete.Field()
