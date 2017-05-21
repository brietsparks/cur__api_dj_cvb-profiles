import graphene

from profiles.exceptions import DoesNotExistError
from profiles.managers.contribution import ContributionManager # create_contribution, delete_contribution


class ContributionType(graphene.ObjectType):
    uuid = graphene.ID(required=True)
    title = graphene.String(required=True)
    summary = graphene.String()


class CreateContributionMutation(graphene.Mutation):
    class Input:
        projectUuid = graphene.ID(required=True)
        title = graphene.String(required=True)

    # return types
    ok = graphene.Boolean()
    message = graphene.String()
    contribution = graphene.Field(lambda: ContributionType)

    @staticmethod
    def mutate(root, args, context, info):
        ok = False
        message = None
        new_contribution = None

        try:
            ContributionManager.create_contribution(
                title=args['title'],
                project_uuid=args['projectUuid']
            )
            ok = True
        except DoesNotExistError as e:
            message = e

        return CreateContributionMutation(contribution=new_contribution, ok=ok, message=message)


class DeleteContributionMutation(graphene.Mutation):
    class Input:
        uuid = graphene.ID(required=True)

    # return types
    ok = graphene.Boolean()
    message = graphene.String()

    @staticmethod
    def mutate(root, args, context, info):
        ok = False
        message = None

        try:
            ContributionManager.delete_contribution(uuid=args['uuid'])
            ok = True
        except DoesNotExistError as e:
            message = e

        return DeleteContributionMutation(ok=ok, message=message)
