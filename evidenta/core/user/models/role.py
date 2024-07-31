from django.contrib.auth.models import Permission
from django.db import models

from evidenta.common.models.base import BaseModel
from evidenta.core.user.enums import UserRole


class Role(BaseModel):
    name = models.CharField(choices=UserRole.choices, unique=True, max_length=20)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other):
        return self.name == other

    def __hash__(self):
        return super().__hash__()
