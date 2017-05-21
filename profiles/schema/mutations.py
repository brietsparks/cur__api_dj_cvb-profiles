import graphene

from .project import (
    CreateProjectMutation,
    DeleteProjectMutation
)

from .contribution import (
    CreateContributionMutation,
    DeleteContributionMutation
)


class Mutations(graphene.AbstractType):
    create_project = CreateProjectMutation.Field()
    delete_project = DeleteProjectMutation.Field()
    create_contribution = CreateContributionMutation.Field()
    delete_contribution = DeleteContributionMutation.Field()
