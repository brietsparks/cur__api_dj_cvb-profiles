import graphene
from .models import Profile as ProfileModel
from exps.schema import Query as ProjectQuery, ProjectType


class ProfileType(graphene.ObjectType):
    uuid = graphene.ID(required=True)
    name = graphene.String()
    projects = graphene.List(ProjectType)


class QueryType(graphene.ObjectType, ProjectQuery):
    profile = graphene.Field(ProfileType, uuid=graphene.ID(required=True))

    def resolve_profile(self, args, context, info):
        profile_uuid = args.get('uuid')
        return ProfileModel.nodes.get_or_none(uuid=profile_uuid)
