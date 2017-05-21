from profiles.models import Project, Contribution
from profiles.exceptions import DoesNotExistError


class ContributionManager:
    @staticmethod
    def create_contribution(title, project_uuid):
        # guards
        project = Project.nodes.get_or_none(uuid=project_uuid)
        if not project:
            raise DoesNotExistError("Could not add contribution to project with uuid " + project_uuid + " because the project could not be fetched")

        profile = project.profile.get_or_none()
        if not profile:  # not covered in test
            raise DoesNotExistError("Could not add contribution to project with uuid " + project_uuid + " becuase the project does not have a reference to a profile")

        new_contribution = Contribution(title=title).save()

        new_contribution.profile.connect(profile)
        new_contribution.parent_project.connect(project)

        return new_contribution


    @staticmethod
    def delete_contribution(uuid):
        # guards
        contribution = Contribution.nodes.get_or_none(uuid=uuid)
        if not contribution:
            raise DoesNotExistError("Could not delete contribution with uuid " + uuid + " because contribution could not be fetched")

        # delete
        contribution.delete()
