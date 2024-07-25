from functools import wraps
from typing import Callable

from evidenta.common.enums import ApiErrorCode
from evidenta.common.exceptions import PermissionDeniedAPIException


def login_required(fnc: Callable) -> Callable:
    @wraps(fnc)
    def wrapper(cls, arg, info, *args, **kwargs):
        if info.context.user.is_anonymous:
            raise PermissionDeniedAPIException(message="User is not logged in.", error_code=ApiErrorCode.LOGIN_REQUIRED)
        return fnc(cls, arg, info, *args, **kwargs)

    return wrapper


def permissions_required(permissions: list[str]) -> Callable:
    def decorator(fnc: Callable) -> Callable:
        @wraps(fnc)
        def wrapper(cls, arg, info, *args, **kwargs):
            if not info.context.user.has_perms(permissions):
                raise PermissionDeniedAPIException(
                    message=f"User '{info.context.user.username}' does not have required permissions.",
                    error_code=ApiErrorCode.PERMISSION_REQUIRED,
                )
            return fnc(cls, arg, info, *args, **kwargs)

        return wrapper

    return decorator
