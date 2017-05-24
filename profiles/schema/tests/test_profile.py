from django.test import TestCase
from neomodel import db, clear_neo4j_database


class CreateProfileMutationTest(TestCase):
    def setUp(self):
        clear_neo4j_database(db)

    def test_create_profile_unauthorized(self):
        pass