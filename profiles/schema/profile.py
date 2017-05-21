import graphene
from profiles.models import Profile as ProfileModel
from .project import ProjectType
from .email_address import EmailAddressType
from profiles.managers.profile import ProfileManager


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


class CreateProfileMutation(graphene.Mutation):
    class Input:
        email = graphene.String(required=True)

    # return types
    ok = graphene.Boolean()
    message = graphene.String()
    profile_uuid = graphene.ID()

    @staticmethod
    def mutate(root, args, context, info):
        ok = False
        message = None
        profile_uuid = None

        try:
            profile_uuid = ProfileManager.create_new_profile(email=args['email'])
            ok = True
        except Exception as e:
            message = 'An unexpected error occurred'

        return CreateProfileMutation(profile_uuid=profile_uuid, ok=ok, message=message)
