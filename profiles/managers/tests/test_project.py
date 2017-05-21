from django.test import TestCase
from neomodel import db, clear_neo4j_database
from profiles.models import Profile, Project, Contribution
from profiles.managers.project import ProjectManager  # create_project, delete_project
from profiles.exceptions import DoesNotExistError, RelationshipConstraintError
from profiles.util import shuffle_string


class CreateProjectTestCase(TestCase):

    profile = None
    parent_project = None

    def setUp(self):
        clear_neo4j_database(db)

        profile = Profile().save()
        parent_project = Project(title='parent project').save()

        parent_project.profile.connect(profile)

        self.profile = profile
        self.parent_project = parent_project

    def test_create_project_happy_no_parent_project(self):
        profile = self.profile
        project = ProjectManager.create_project(profile.uuid, 'project')

        # persistence
        self.assertEqual(Project.nodes.get(uuid=project.uuid), project)

        # property
        self.assertEqual(project.title, 'project')

        # relationships
        self.assertEqual(project.profile.get(), profile)
        self.assertIn(project, profile.projects.all())

    def test_create_project_happy_with_parent_project(self):
        profile = self.profile
        parent_project = self.parent_project
        project = ProjectManager.create_project(profile.uuid, 'project', self.parent_project.uuid)

        # persistence
        self.assertEqual(Project.nodes.get(uuid=project.uuid), project)

        # property
        self.assertEqual(project.title, 'project')

        # relationships
        self.assertEqual(project.profile.get(), profile)
        self.assertIn(project, profile.projects.all())
        self.assertEqual(project.parent_project.get(), parent_project)
        self.assertIn(project, parent_project.child_projects.all())

    def test_create_project_error_when_missing_profile(self):
        bad_uuid = shuffle_string(self.profile.uuid)

        with self.assertRaises(DoesNotExistError):
            project = ProjectManager.create_project(bad_uuid, 'project')

    def test_create_project_error_when_missing_parent_project(self):
        bad_uuid = shuffle_string(self.parent_project.uuid)

        with self.assertRaises(DoesNotExistError):
            project = ProjectManager.create_project(self.profile.uuid, 'project', bad_uuid)


class DeleteProjectTestCase(TestCase):

    profile = None
    parent_project = None

    def setUp(self):
        clear_neo4j_database(db)

        project = Project(title='parent').save()
        self.project = project

    def test_delete_project_happy(self):
        uuid = self.project.uuid
        ProjectManager.delete_project(uuid)
        self.assertIsNone(Project.nodes.get_or_none(uuid=uuid))

    def test_delete_project_error_when_missing(self):
        bad_uuid = shuffle_string(self.project.uuid)

        with self.assertRaises(DoesNotExistError):
            ProjectManager.delete_project(bad_uuid)

    def test_delete_project_error_when_child_project(self):
        project = self.project
        child_project = Project(title='child parent').save()
        project.child_projects.connect(child_project)

        with self.assertRaises(RelationshipConstraintError):
            ProjectManager.delete_project(project.uuid)

    def test_delete_project_error_when_contribution(self):
        project = self.project
        contribution = Contribution(title='contribution').save()
        project.contributions.connect(contribution)

        with self.assertRaises(RelationshipConstraintError):
            ProjectManager.delete_project(project.uuid)
