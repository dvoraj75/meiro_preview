from unittest.mock import patch

from django.test import Client

import pytest
from graphene_django.utils.testing import graphql_query

from evidenta.common.enums import ERROR_MESSAGES, ApiErrorCode
from evidenta.common.schemas.utils import get_error_message_from_error_code
from evidenta.common.testing.utils import (
    assert_equal,
    assert_exist,
    assert_match,
    extract_error_code_from_graphql_error_response,
)
from evidenta.core.user.enums import UserRole
from evidenta.core.user.models import User
from evidenta.core.user.service import UserService


@pytest.mark.django_db
def test_update_user_mutation_should_return_user(
    django_client: Client, admin: User, mock_function_create_or_update, update_user_mutation_query
) -> None:
    django_client.force_login(admin)
    with patch.object(UserService, "update", mock_function_create_or_update):
        result = graphql_query(update_user_mutation_query, client=django_client)
        assert_exist(result.json().get("data"))


@pytest.mark.django_db
def test_update_user_mutation_should_raise_object_does_not_exist_api_exception_for_non_existing_user(
    django_client: Client, admin: User, mock_function_create_or_update, update_user_mutation_query
):
    django_client.force_login(admin)
    with patch.object(UserService, "update", side_effect=User.DoesNotExist):
        result = graphql_query(update_user_mutation_query, client=django_client)
        assert_equal(result.status_code, 400)
        assert_equal(extract_error_code_from_graphql_error_response(result.json()), ApiErrorCode.OBJECT_NOT_FOUND.value)


@pytest.mark.django_db
def test_update_user_mutation_should_raise_invalid_data_api_exception_when_except_validation_error(
    django_client: Client, admin: User, mock_function_invalid_data_error, update_user_mutation_query
) -> None:
    django_client.force_login(admin)
    with patch.object(UserService, "update", mock_function_invalid_data_error):
        result = graphql_query(update_user_mutation_query, client=django_client).json()
        assert_exist(result.get("errors"))
        assert_equal(
            result.get("errors")[0].get("error_data")[0].get("code"),
            ApiErrorCode.INVALID_VALUES.value,
        )
        assert_equal(
            result.get("errors")[0].get("error_data")[0].get("message"),
            ERROR_MESSAGES[ApiErrorCode.INVALID_VALUES],
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "error", [ValueError("Some value error"), TypeError("Some type error"), KeyError("Some key error")]
)
def test_update_user_mutation_should_raise_unexpected_api_error_when_except_random_error(
    django_client: Client, admin: User, update_user_mutation_query, error
) -> None:
    django_client.force_login(admin)
    with patch.object(UserService, "update", side_effect=error):
        result = graphql_query(update_user_mutation_query, client=django_client).json()
        assert_exist(result.get("errors"))
        for e in result.get("errors"):
            assert_equal(
                get_error_message_from_error_code(ApiErrorCode.UNEXPECTED_ERROR, error=str(error)),
                e.get("message"),
            )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "update_user_mutation_query",
    [
        {"exclude": ("userId",)},
    ],
    indirect=True,
)
def test_update_user_mutation_should_fail_when_missing_required_field(
    django_client: Client, admin: User, update_user_mutation_query
) -> None:
    django_client.force_login(admin)
    response = graphql_query(update_user_mutation_query, client=django_client).json()
    assert_exist(response.get("errors"))
    for e in response.get("errors"):
        assert_match(r"^Field.+not provided.$", e.get("message"))


@pytest.mark.parametrize(
    "update_user_mutation_query",
    [
        {"extra": {"vyska": 130}},
        {"extra": {"pocet": "nekolik"}},
    ],
    indirect=True,
)
def test_update_user_mutation_should_fail_when_get_unknown_field(django_client, update_user_mutation_query) -> None:
    response = graphql_query(update_user_mutation_query).json()
    assert_exist(response.get("errors"))
    for e in response.get("errors"):
        assert_match(r"^Field.+not defined.+$", e.get("message"))


@pytest.mark.django_db
@pytest.mark.parametrize(
    "update_user_mutation_query",
    [
        {"extra": {"companies": [1, 2, 3]}},
    ],
    indirect=True,
)
def test_update_user_mutation_should_fail_with_permission_denied_if_user_without_permissions_set_companies(
    django_client,
    guest,
    update_user_mutation_query,
) -> None:
    guest.add_permission("change_user")
    django_client.force_login(guest)
    response = graphql_query(update_user_mutation_query, client=django_client).json()
    assert_exist(response.get("errors"))
    for e in response.get("errors"):
        assert_equal(ApiErrorCode.PERMISSION_REQUIRED, e.get("error_code"))


@pytest.mark.django_db
@pytest.mark.parametrize(
    "update_user_mutation_query",
    [
        {"extra": {"role": UserRole.GUEST}},
    ],
    indirect=True,
)
def test_update_user_mutation_should_fail_with_permission_denied_if_user_without_permissions_set_role(
    django_client,
    guest,
    update_user_mutation_query,
) -> None:
    guest.add_permission("change_user")
    django_client.force_login(guest)
    response = graphql_query(update_user_mutation_query, client=django_client).json()
    assert_exist(response.get("errors"))
    for e in response.get("errors"):
        assert_equal(ApiErrorCode.PERMISSION_REQUIRED, e.get("error_code"))


@pytest.mark.django_db
@pytest.mark.parametrize(
    "update_user_mutation_query",
    [
        {"extra": {"role": UserRole.SUPERVISOR}},
    ],
    indirect=True,
)
def test_update_user_mutation_should_fail_with_permission_denied_if_user_without_permissions_set_supervisor_role(
    django_client,
    guest,
    update_user_mutation_query,
) -> None:
    guest.add_permission("add_user")
    guest.add_permission("assign_role")
    django_client.force_login(guest)
    response = graphql_query(update_user_mutation_query, client=django_client).json()
    assert_exist(response.get("errors"))
    for e in response.get("errors"):
        assert_equal(ApiErrorCode.PERMISSION_REQUIRED, e.get("error_code"))
