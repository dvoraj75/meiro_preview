from unittest.mock import patch

from django.test import Client

import pytest
from graphene_django.utils.testing import graphql_query

from evidenta.common.enums import ApiErrorCode
from evidenta.common.schemas.utils import get_error_message_from_error_code
from evidenta.common.testing.utils import assert_equal, assert_exist, extract_error_code_from_graphql_error_response
from evidenta.core.user.models import User
from evidenta.core.user.service import UserService


@pytest.mark.django_db
def test_delete_user_mutation_should_successfully_pass(
    django_client: Client, admin: User, mock_function_create_or_update, delete_user_mutation_query
) -> None:
    django_client.force_login(admin)
    with patch.object(UserService, "delete", mock_function_create_or_update):
        result = graphql_query(delete_user_mutation_query, client=django_client)
        assert_exist(result.json().get("data"))


@pytest.mark.django_db
def test_delete_user_mutation_should_raise_object_does_not_exist_api_exception_for_non_existing_user(
    django_client: Client, admin: User, mock_function_create_or_update, delete_user_mutation_query
):
    django_client.force_login(admin)
    with patch.object(UserService, "delete", side_effect=User.DoesNotExist):
        result = graphql_query(delete_user_mutation_query, client=django_client)
        assert_equal(result.status_code, 400)
        assert_equal(extract_error_code_from_graphql_error_response(result.json()), ApiErrorCode.OBJECT_NOT_FOUND.value)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "error", [ValueError("Some value error"), TypeError("Some type error"), KeyError("Some key error")]
)
def test_delete_user_mutation_should_raise_unexpected_api_error_when_except_random_error(
    django_client: Client, admin: User, delete_user_mutation_query, error
) -> None:
    django_client.force_login(admin)
    with patch.object(UserService, "delete", side_effect=error):
        result = graphql_query(delete_user_mutation_query, client=django_client).json()
        assert_exist(result.get("errors"))
        for e in result.get("errors"):
            assert_equal(
                get_error_message_from_error_code(ApiErrorCode.UNEXPECTED_ERROR, error=str(error)),
                e.get("message"),
            )
