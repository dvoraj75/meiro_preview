from django.conf import settings
from django.contrib.auth.models import Permission

from evidenta.core.user.enums import UserRole
from evidenta.core.user.models import Role, User

from .enums import BASE_USERS_DATA, ROLES_AND_PERMISSIONS


def create_base_data(**kwargs) -> None:
    create_roles_and_permissions()
    create_base_users(**kwargs)


def create_roles_and_permissions() -> None:
    for role_name, permissions in ROLES_AND_PERMISSIONS.items():
        print(f"Creating '{role_name}' role")  # noqa: T201
        role, created = Role.objects.get_or_create(name=role_name)
        for perm_name in permissions:
            try:
                perm = Permission.objects.get(codename=perm_name)
                role.permissions.add(perm)
            except Permission.DoesNotExist:
                print(f"Permission {perm_name} not found")  # noqa: T201


def create_base_users() -> None:
    if settings.PRODUCTION or not settings.DEBUG:
        print(f"Can't create base users with PRODUCTION={settings.PRODUCTION} and DEBUG={settings.DEBUG}")  # noqa: T201
        return
    for user_data in BASE_USERS_DATA:
        print(f"Creating '{user_data['username']}' user")  # noqa: T201
        create = User.objects.create
        if user_data.get("role") == UserRole.ADMIN:
            user_data["is_superuser"] = True
            user_data["is_staff"] = True
        create(password=f"evidenta{user_data.get('username')}123", **user_data)
