from django.contrib.auth.models import Permission

from evidenta.core.user.enums import UserRole
from evidenta.core.user.models import Role


def get_roles_and_permissions() -> dict[str, list[str]]:
    return {
        UserRole.GUEST: [
            "change_user",
        ],
        UserRole.CLIENT: [
            "view_company",
            "change_company",
            "view_user",
            "change_user",
        ],
        UserRole.ACCOUNTANT: [
            "view_company",
            "change_company",
            "view_user",
            "change_user",
        ],
        UserRole.SUPERVISOR: [
            "add_company",
            "view_company",
            "change_company",
            "delete_company",
            "add_user",
            "view_user",
            "change_user",
            "delete_user",
        ],
        UserRole.ADMIN: [],
    }


def create_roles_and_permissions():
    roles_and_permissions = get_roles_and_permissions()
    for role_name, permissions in roles_and_permissions.items():
        role, created = Role.objects.get_or_create(name=role_name)
        for perm_name in permissions:
            try:
                perm = Permission.objects.get(codename=perm_name)
                role.permissions.add(perm)
            except Permission.DoesNotExist:
                print(f"Permission {perm_name} not found")  # noqa: T201
