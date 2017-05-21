from django.test import TestCase
from neomodel import db, clear_neo4j_database
from profiles.models import Profile, EmailAddress
from profiles.managers.profile import ProfileManager


class CreateProfileTest(TestCase):

    def setUp(self):
        clear_neo4j_database(db)

    def test_create_profile_with_new_email_address(self):
        value = 'test@test.test'

        new_profile_uuid = ProfileManager.create_new_profile(value)
        new_profile = Profile.nodes.get(uuid=new_profile_uuid)
        email_address = new_profile.email_addresses.get(value=value)
        self.assertEqual(email_address.value, value)

    def test_create_profile_with_existing_email_address(self):
        value = 'test@test.test'
        email_address = EmailAddress(value=value).save()

        new_profile_uuid = ProfileManager.create_new_profile(value)
        new_profile = Profile.nodes.get(uuid=new_profile_uuid)
        email_address = new_profile.email_addresses.get(value=value)
        self.assertEqual(email_address.value, value)
