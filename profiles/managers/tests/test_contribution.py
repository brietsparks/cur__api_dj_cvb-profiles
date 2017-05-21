from django.test import TestCase
from neomodel import db, clear_neo4j_database
from profiles.models import Profile
from profiles.models import Project, Contribution
from profiles.managers.contribution import ContributionManager  # create_contribution, delete_contribution
from profiles.exceptions import DoesNotExistError
from profiles.util import shuffle_string


class CreateContributionTest(TestCase):
    
    profile = None
    project = None

    def setUp(self):
        clear_neo4j_database(db)

        profile = Profile().save()
        project = Project(title='project').save()

        project.profile.connect(profile)

        self.profile = profile
        self.project = project

    def test_create_contribution_happy(self):
        project = self.project
        profile = self.profile

        contribution = ContributionManager.create_contribution('contribution', project.uuid)

        # persistence
        self.assertEqual(Contribution.nodes.get(uuid=contribution.uuid), contribution)

        # property
        self.assertEqual(contribution.title, 'contribution')

        # relationships
        self.assertEqual(contribution.profile.get(), profile)
        self.assertIn(contribution, profile.contributions.all())

        self.assertEqual(contribution.parent_project.get(), project)
        self.assertIn(contribution, project.contributions.all())

    def test_create_contribution_errors_when_project_bad_uuid(self):
        bad_project_uuid = shuffle_string(self.project.uuid)

        with self.assertRaises(DoesNotExistError):
            ContributionManager.create_contribution('contribution', bad_project_uuid)


class DeleteContributionTest(TestCase):

    contribution = None
    profile = None
    project = None

    def setUp(self):
        clear_neo4j_database(db)

        profile = Profile().save()
        project = Project(title='project').save()
        contribution = Contribution(title='contribution').save()

        project.profile.connect(profile)

        contribution.parent_project.connect(project)

        self.profile = profile
        self.project = project
        self.contribution = contribution

    def test_delete_contribution_happy(self):
        uuid = self.contribution.uuid
        ContributionManager.delete_contribution(uuid)
        self.assertIsNone(Contribution.nodes.get_or_none(uuid=uuid))

    def test_delete_project_error_when_missing(self):
        bad_uuid = shuffle_string(self.contribution.uuid)

        with self.assertRaises(DoesNotExistError):
            ContributionManager.delete_contribution(bad_uuid)
