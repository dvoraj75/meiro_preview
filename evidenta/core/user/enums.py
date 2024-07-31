from enum import Enum, auto

from django.db.models import IntegerChoices, TextChoices
from django.utils.translation import gettext_lazy as _


class UserRole(TextChoices):
    GUEST = "guest", _("Guest")
    CLIENT = "client", _("Client")
    ACCOUNTANT = "accountant", _("Accountant")
    SUPERVISOR = "supervisor", _("Supervisor")
    ADMIN = "admin", _("Admin")


class UserGender(IntegerChoices):
    MALE = auto(), _("Male")
    FEMALE = auto(), _("Female")


class ResourcePath(Enum):
    SETUP_PASSWORD = "/setup-password/{token}"  # noqa: S105
    RESET_PASSWORD = "/reset-password/{token}"  # noqa: S105

    def format(self, **kwargs) -> str:
        return self.value.format(**kwargs)
