from django.core.exceptions import ValidationError

import pytest

from evidenta.common.testing.utils import assert_count
from evidenta.core.user.enums import UserRole
from evidenta.core.user.models import Role


@pytest.mark.django_db
@pytest.mark.usefixtures("drop_all_roles")
@pytest.mark.parametrize("role_name", [*UserRole])
def test_create_role_should_successfully_pass_for_valid_role_name(role_name: UserRole) -> None:
    Role.objects.create(name=role_name)
    assert_count(Role.objects.filter(), 1)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "role_name",
    [
        "test1",
    ],
)
def test_create_role_should_fail_with_validation_error_for_invalid_role_name(role_name: str) -> None:
    with pytest.raises(ValidationError):
        Role.objects.create(name=role_name)


@pytest.mark.django_db
@pytest.mark.parametrize("role_name", [*UserRole])
def test_create_role_should_fail_with_validation_error_for_non_unique_name(role_name: UserRole) -> None:
    with pytest.raises(ValidationError):
        Role.objects.create(name=role_name)
        assert_count(Role.objects.filter(), len(UserRole))
