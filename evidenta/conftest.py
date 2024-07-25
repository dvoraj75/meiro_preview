from unittest.mock import MagicMock

from django.conf import settings
from django.core.management import call_command
from django.test import Client

import pytest
import pytest_django
from _pytest.fixtures import SubRequest

from evidenta.common.utils.tests import generate_random_company_data, generate_random_user_data
from evidenta.core.company.models import Company
from evidenta.core.user.enums import UserRole
from evidenta.core.user.models import Role, User
from evidenta.initial_data import create_roles_and_permissions


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker: pytest_django.plugin.DjangoDbBlocker) -> None:
    with django_db_blocker.unblock():
        for fixture in settings.TEST_FIXTURES_FILES:
            call_command("loaddata", fixture)


@pytest.fixture
def setup_roles():
    create_roles_and_permissions()


@pytest.fixture
def django_client():
    return Client()


@pytest.fixture
def empty_filter_mock():
    magic = MagicMock()
    magic.filter.return_value = magic
    return magic


@pytest.fixture
def admin() -> User:
    user_data = generate_random_user_data()
    admin_role = Role.objects.get(name=UserRole.ADMIN)
    user_data.update({"username": "admin", "role": admin_role, "email": "admin@admin.cz"})
    return User.objects.create_superuser(**user_data)


@pytest.fixture
def supervisor() -> User:
    user_data = generate_random_user_data()
    user_data.update({"username": "supervisor", "role": UserRole.SUPERVISOR})
    return User.objects.create(**user_data)


@pytest.fixture
def accountant() -> User:
    user_data = generate_random_user_data()
    user_data.update({"username": "accountant", "role": UserRole.ACCOUNTANT})
    return User.objects.create(**user_data)


@pytest.fixture
def client() -> User:
    user_data = generate_random_user_data()
    user_data.update({"username": "client", "role": UserRole.CLIENT})
    return User.objects.create(**user_data)


@pytest.fixture
def guest() -> User:
    user_data = generate_random_user_data()
    user_data.update({"username": "guest", "role": UserRole.GUEST})
    return User.objects.create(**user_data)


@pytest.fixture
def user_data(request: SubRequest) -> dict[str, any]:
    user_data = generate_random_user_data()
    if hasattr(request, "param"):
        user_data.update(request.param)
    return user_data


@pytest.fixture
def super_user_data(request: SubRequest, user_data: dict[str, any]) -> dict[str, any]:
    user_data.update(
        {
            "username": "JohnDoeAdmin",
            "role": UserRole.ADMIN,
        }
    )
    if hasattr(request, "param"):
        user_data.update(request.param)
    return user_data


@pytest.fixture
def user_data_with_companies(
    request: SubRequest, user_data: dict[str, any], random_companies: list[Company]
) -> dict[str, any]:
    user_data.update({"companies": random_companies})
    if hasattr(request, "param"):
        user_data.update(request.param)
    return user_data


def _create_user(**user_data: dict[str, any]) -> User:
    return User.objects.create(**user_data)


@pytest.fixture
def random_user(user_data: dict[str, any]) -> User:
    return _create_user(**user_data)


@pytest.fixture
def random_users(request: SubRequest) -> list[User]:
    return [
        _create_user(**generate_random_user_data()) for _ in range(request.param if hasattr(request, "param") else 2)
    ]


@pytest.fixture
def company_data(request: SubRequest) -> dict[str, any]:
    return generate_random_company_data()


def _create_company(**company_data: dict[str, any]) -> Company:
    return Company.objects.create(**company_data)


@pytest.fixture
def random_company(company_data) -> Company:
    return _create_company(**company_data)


@pytest.fixture
def random_companies(request: SubRequest) -> list[Company]:
    return [
        _create_company(**generate_random_company_data())
        for _ in range(request.param if hasattr(request, "param") else 2)
    ]
