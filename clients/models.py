from django.db import models
import uuid


class ClientManager(models.Manager):
    def authenticate(self, client_id, secret_attempt):
        """
        Authenticate a client instance by hashing a raw secret and
        comparing it to the client's hashed secret
        """
        try:
            client = self.get(pk=client_id)
        except Client.DoesNotExist:
            return False

        if client.secret == secret_attempt:
            return client

        return False


class Permission(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    objects = ClientManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    secret = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=60)
    domain = models.CharField(max_length=255, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def get_granted_permissions(self, requested_names):
        permissions = self.permissions.filter(name__in=requested_names) #.values('name', 'description')

        return permissions

    def __str__(self):
        return self.name