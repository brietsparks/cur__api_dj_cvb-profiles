from profiles.schema.profile import ProfileQuery
from profiles.schema.email_address import EmailAddressQuery
from profiles.schema.mutations import Mutations as ProfileMutations
import graphene


class RootQueryType(
    ProfileQuery,
    EmailAddressQuery,
    graphene.ObjectType
):
    pass


class Mutations(
    ProfileMutations,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=RootQueryType, mutation=Mutations)
