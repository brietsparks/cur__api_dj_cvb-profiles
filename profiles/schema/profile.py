import graphene
from profiles.models import Profile as ProfileModel
from .project import ProjectType
from .email_address import EmailAddressType


class ProfileType(graphene.ObjectType):
    uuid = graphene.ID(required=True)
    name = graphene.String()
    projects = graphene.List(ProjectType)
    email_address = graphene.List(EmailAddressType)


class ProfileQuery(graphene.AbstractType):
    profile = graphene.Field(ProfileType, uuid=graphene.ID(required=True))

    def resolve_profile(self, args, context, info):
        profile_uuid = args.get('uuid')
        return ProfileModel.nodes.get_or_none(uuid=profile_uuid)
