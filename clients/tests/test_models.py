from django.test import TestCase
from clients.models import Client, ClientManager
import uuid


class ClientManagerTest(TestCase):

    def setUp(self):
        self.secret = uuid.uuid4()
        client = Client(secret=self.secret)
        client.save()
        self.client_id = client.id
        self.client = client

    def test_authenticate_correct_secret_returns_true(self):
        self.assertTrue(Client.objects.authenticate(self.client_id, self.secret))

    def test_authenticate_invalid_id_returns_false(self):
        self.assertFalse(Client.objects.authenticate(uuid.uuid4(), self.secret))

    def test_authenticate_incorrect_secret_returns_false(self):
        self.assertFalse(Client.objects.authenticate(self.client_id, uuid.uuid4()))
