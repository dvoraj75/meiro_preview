from typing import cast
from unittest.mock import patch

import pytest
from django_mock_queries.query import MockModel, MockSet

from evidenta.common.utils.tests import assert_count, assert_equal, assert_none, assert_obj_equal
from evidenta.core.user.models import CustomUserManager, User
from evidenta.core.user.service import UserService


SERVICE = UserService()


@pytest.mark.django_db
@pytest.mark.parametrize("user_data,user", [({"data": "some_data"}, cast(User, "user"))])
def test_user_service_create_should_return_new_user(user_data: dict[str, any], user: User) -> None:
    with patch.object(CustomUserManager, "create", return_value=user) as mock_create:
        new_user = SERVICE.create(**user_data)
        mock_create.assert_called_once_with(**user_data)
        assert_equal(user, new_user)


@pytest.mark.django_db
@pytest.mark.parametrize("as_user", [(cast(User, "as_user"))])
def test_user_service_get_should_return_user_by_id(as_user: User, user_data: dict[str, any]) -> None:
    mock = MockModel(pk=1, **user_data)
    with patch.object(CustomUserManager, "get_all_related_users", return_value=MockSet(mock)) as mock_get:
        user = SERVICE.get(user_id=1, as_user=as_user)
        mock_get.assert_called_once_with(as_user=as_user)
        assert_obj_equal(cast(User, mock), user)

        mock_get.asset_called_once_with(as_user=as_user)


@pytest.mark.django_db
@pytest.mark.parametrize("as_user", [cast(User, "as_user")])
def test_user_service_get_all_should_return_all_related_users(as_user: User) -> None:
    with patch.object(
        CustomUserManager, "get_all_related_users", return_value=MockSet(MockModel(), MockModel())
    ) as mock_get_all:
        users = SERVICE.get_all(as_user=as_user)
        mock_get_all.assert_called_once_with(as_user=as_user)
        assert_count(users, 2)


@pytest.mark.django_db
@pytest.mark.parametrize("as_user,user_data", [(cast(User, "as_user"), {"data": "some_data"})])
def test_user_service_update_should_return_none_for_successful_update(as_user: User, user_data: dict[str, any]) -> None:
    with patch.object(CustomUserManager, "update", return_value=None) as mock_update:
        assert_none(SERVICE.update(user_id=1, as_user=as_user, **user_data))
        mock_update.assert_called_once_with(user_id=1, as_user=as_user, **user_data)


@pytest.mark.django_db
@pytest.mark.parametrize("as_user", [cast(User, "as_user")])
def test_user_service_delete_should_return_none_for_successful_delete(as_user: User) -> None:
    with patch.object(CustomUserManager, "delete", return_value=None) as mock_update:
        assert_none(SERVICE.delete(user_id=1, as_user=as_user))
        mock_update.assert_called_once_with(user_id=1, as_user=as_user)
