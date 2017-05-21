from profiles.models import Profile, Project
from profiles.exceptions import DoesNotExistError, RelationshipConstraintError


class ProjectManager:
    @staticmethod
    def create_project(profile_uuid, title, parent_project_uuid=None):
        # guards
        profile = Profile.nodes.get_or_none(uuid=profile_uuid)
        if not profile:
            raise DoesNotExistError("Could not fetch profile with uuid " + profile_uuid)

        parent_project = None
        if parent_project_uuid:
            parent_project = Project.nodes.get_or_none(uuid=parent_project_uuid)
            if not parent_project:
                raise DoesNotExistError("Could not fetch parent_project with uuid " + parent_project_uuid)

        # create
        new_project = Project(title=title).save()

        new_project.profile.connect(profile)

        if parent_project:
            new_project.parent_project.connect(parent_project)

        return new_project

    @staticmethod
    def delete_project(uuid):
        # guards
        project = Project.nodes.get_or_none(uuid=uuid)
        if not project:
            raise DoesNotExistError("Could not fetch project with uuid " + uuid)

        if project.child_projects or project.contributions:
            raise RelationshipConstraintError("Could not delete project with uuid " + uuid + " because it still has child nodes")

        # delete
        project.delete()
