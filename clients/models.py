from django.db import models
import uuid


class Permission(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_secret = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=60)
    domain = models.CharField(max_length=255, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

