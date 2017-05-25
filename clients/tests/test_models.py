from django.test import TestCase, SimpleTestCase
from clients.models import Client, ClientManager, Permission
import uuid


class ClientManagerTest(TestCase):

    def setUp(self):
        secret = uuid.uuid4()
        client = Client(secret=secret)
        client.save()

        self.secret = secret
        self.client_id = client.id
        self.client = client

    def test_authenticate_correct_secret_returns_true(self):
        self.assertTrue(Client.objects.authenticate(self.client_id, self.secret))

    def test_authenticate_invalid_id_returns_false(self):
        self.assertFalse(Client.objects.authenticate(uuid.uuid4(), self.secret))

    def test_authenticate_incorrect_secret_returns_false(self):
        self.assertFalse(Client.objects.authenticate(self.client_id, uuid.uuid4()))


class ClientTest(TestCase):

    def setUp(self):
        pass
        permission_1 = Permission(name='permission_1', description='permission 1 description')
        permission_1.save()
        permission_2 = Permission(name='permission_2', description='permission 2 description')
        permission_2.save()
        permission_3 = Permission(name='permission_3', description='permission 3 description')
        permission_3.save()

        client = Client()
        client.save()
        client.permissions.add(permission_1)
        client.permissions.add(permission_2)
        client.permissions.add(permission_3)

        self.permission_1 = permission_1
        self.permission_2 = permission_2
        self.permission_3 = permission_3
        self.client = client

    def test_get_granted_permissions_returns_granted_permissions(self):
        # actual
        granted_permissions_query_set = self.client.get_granted_permissions([
            self.permission_1.name,
            self.permission_2.name
        ]).values('name', 'description')

        granted_permissions_list = list(granted_permissions_query_set)

        # expected
        expected = [
            {'name': self.permission_1.name, 'description': self.permission_1.description},
            {'name': self.permission_2.name, 'description': self.permission_2.description}
        ]

        # assertion
        self.assertEqual(
            granted_permissions_list,
            expected
        )

    def test_get_granted_permission_names_does_not_return_an_ungranted_permission_names(self):
        # actual
        granted_permissions_query_set = self.client.get_granted_permissions([
            self.permission_1.name,
            'ungranted_permission'
        ]).values('name', 'description')

        granted_permissions_list = list(granted_permissions_query_set)

        # expected
        expected = [
            {'name': self.permission_1.name, 'description': self.permission_1.description},
        ]

        # assertion
        self.assertEqual(
            granted_permissions_list,
            expected
        )
