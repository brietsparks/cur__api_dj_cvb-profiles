import graphene

from profiles.models import Project as ProjectModel, Profile as ProfileModel

from .project import (
    ProjectType,
    CreateProjectMutation,
    DeleteProjectMutation
)

from .contribution import (
    CreateContributionMutation,
    DeleteContributionMutation
)

from .profile import (
    ProfileType,
)


class Mutations(graphene.AbstractType):
    create_project = CreateProjectMutation.Field()
    delete_project = DeleteProjectMutation.Field()
    create_contribution = CreateContributionMutation.Field()
    delete_contribution = DeleteContributionMutation.Field()


class ProjectQuery(graphene.AbstractType):
    profile = graphene.Field(ProjectType, uuid=graphene.ID(required=True))

    def resolve_project(self, args, context, info):
        project_uuid = args.get('projectUuid')
        return ProjectModel.nodes.get_or_none(uuid=project_uuid)


class ProfileQuery(graphene.ObjectType, ProjectQuery):
    profile = graphene.Field(ProfileType, uuid=graphene.ID(required=True))

    def resolve_profile(self, args, context, info):
        profile_uuid = args.get('uuid')
        return ProfileModel.nodes.get_or_none(uuid=profile_uuid)
