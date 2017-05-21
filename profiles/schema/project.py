import graphene

from profiles.managers.project import ProjectManager # create_project, delete_project
from profiles.models import Project as ProjectModel
from profiles.exceptions import DoesNotExistError, RelationshipConstraintError


class ProjectType(graphene.ObjectType):
    uuid = graphene.ID(required=True)
    title = graphene.String(required=True)
    summary = graphene.String()


class ProjectQuery(graphene.AbstractType):
    project = graphene.Field(ProjectType, uuid=graphene.ID(required=True))

    def resolve_project(self, args, context, info):
        project_uuid = args.get('projectUuid')
        return ProjectModel.nodes.get_or_none(uuid=project_uuid)


# I love you sooooo much, don't change :) well, if change means less programming, then I'd be ok with it ;)
class CreateProjectMutation(graphene.Mutation):
    class Input:
        profileUuid = graphene.ID(required=True)
        title = graphene.String(required=True)
        parentProjectUuid = graphene.ID()

    # return types
    ok = graphene.Boolean()
    message = graphene.String()
    project = graphene.Field(lambda: ProjectType)

    @staticmethod
    def mutate(root, args, context, info):
        new_project = None
        ok = False
        message = None

        parent_project_uuid = None
        if 'parentProjectUuid' in args:
            parent_project_uuid = args['parentProjectUuid']

        try:
            new_project = ProjectManager.create_project(
                profile_uuid=args['profileUuid'],
                title=args['title'],
                parent_project_uuid=parent_project_uuid
            )
            ok = True
        except DoesNotExistError as e:
            message = e

        return CreateProjectMutation(project=new_project, ok=ok, message=message)


class DeleteProjectMutation(graphene.Mutation):
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
            ProjectManager.delete_project(args['uuid'])
            ok = True
        except DoesNotExistError or RelationshipConstraintError as e:
            message = e

        return DeleteProjectMutation(ok=ok, message=message)
