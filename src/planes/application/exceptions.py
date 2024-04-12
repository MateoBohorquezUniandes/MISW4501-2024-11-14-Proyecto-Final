from http import HTTPStatus
from seedwork.presentation.exceptions import APIError


class UnprocessableEntityError(APIError):
    def __init__(self, message=HTTPStatus.UNPROCESSABLE_ENTITY.phrase, code=""):
        super().__init__(HTTPStatus.UNPROCESSABLE_ENTITY.value, message, code)


class BadRequestError(APIError):
    def __init__(self, message=HTTPStatus.BAD_REQUEST.phrase, code=""):
        super().__init__(HTTPStatus.BAD_REQUEST.value, message, code)

class UserNotFoundError(APIError):
    def __init__(self, message=HTTPStatus.NOT_FOUND.phrase):
        super().__init__(HTTPStatus.NOT_FOUND.value, message, "user.not_found")

class UserNotAsociatedError(APIError):
    def __init__(self, message=HTTPStatus.UNPROCESSABLE_ENTITY.phrase):
        super().__init__(HTTPStatus.UNPROCESSABLE_ENTITY.value, message, "user.not_asociated_to_plan")
