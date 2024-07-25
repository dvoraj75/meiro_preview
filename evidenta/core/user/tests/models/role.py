from django.db import IntegrityError

import pytest

from evidenta.common.utils.tests import assert_count
from evidenta.core.user.models import Role


@pytest.mark.django_db
@pytest.mark.parametrize(
    "role_name",
    [
        "test1",
    ],
)
def test_create_role_with_name_should_successfully_pass(role_name: str) -> None:
    Role.objects.create(name=role_name)
    assert_count(Role.objects.filter(name=role_name), 1)


@pytest.mark.django_db
@pytest.mark.usefixtures("setup_roles")
@pytest.mark.parametrize("role_name", ["admin", "supervisor", "accountant", "client", "guest"])
def test_create_role_should_fail_with_integrity_error_for_non_unique_name(role_name: str) -> None:
    with pytest.raises(IntegrityError):
        Role.objects.create(name=role_name)
