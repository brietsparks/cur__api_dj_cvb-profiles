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
        permission_1 = Permission(name='permission_1')
        permission_1.save()
        permission_2 = Permission(name='permission_2')
        permission_2.save()
        permission_3 = Permission(name='permission_3')
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

    def test_get_permissions_returns_permissions_by_given_names(self):
        names = ['permission_1', 'permission_2']
        self.assertEqual(
            self.client.get_permissions(names),
            [self.permission_1, self.permission_2]
        )

    def test_get_permissions_does_not_return_an_ungranted_permission(self):
        names = ['permission_1', 'ungranted-permission']
        self.assertEqual(
            self.client.get_permissions(names),
            [self.permission_1]
        )
