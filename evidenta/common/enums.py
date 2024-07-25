from enum import Enum


class ApiErrorCode(Enum):
    OBJECT_NOT_FOUND = "object_not_found"
    LOGIN_REQUIRED = "login_required"
    PERMISSION_REQUIRED = "permission_required"
    UNEXPECTED_ERROR = "unexpected_error"
