from enum import Enum

from evidenta.core.user.enums import UserRole


class BaseUsers(Enum):
    GUEST = "guest"
    CLIENT = "client"
    ACCOUNTANT = "accountant"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"

    def capitalize(self) -> str:
        return self.value.capitalize()


BASE_USERS_DATA = (
    {
        "username": val.value,
        "first_name": val.capitalize(),
        "last_name": val.capitalize(),
        "role": UserRole(val.value),
        "email": f"{val.value}@{val.value}.cz",
    }
    for val in BaseUsers
)


ROLES_AND_PERMISSIONS = {
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
        "assign_role",
        "assign_supervisor",
        "assign_company_user",
    ],
    UserRole.ADMIN: [],
}
