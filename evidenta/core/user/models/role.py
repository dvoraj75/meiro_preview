from django.contrib.auth.models import Permission
from django.db import models

from evidenta.core.user.enums import UserRole


class Role(models.Model):
    name = models.CharField(choices=UserRole.choices, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other):
        return self.name == other
