from profiles.schema.schema import ProfileQuery
from profiles.schema.schema import Mutations as ProfileMutations
import graphene


class RootQueryType(
    ProfileQuery,
    graphene.ObjectType
):
    pass


class Mutations(
    ProfileMutations,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=RootQueryType, mutation=Mutations)
