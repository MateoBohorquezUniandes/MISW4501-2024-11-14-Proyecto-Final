from http import HTTPStatus
from seedwork.presentation.exceptions import APIError


class UnprocessableEntityError(APIError):
    def __init__(self, message=HTTPStatus.UNPROCESSABLE_ENTITY.phrase, code=""):
        super().__init__(HTTPStatus.UNPROCESSABLE_ENTITY.value, message, code)


class InvalidCredentialsError(APIError):
    def __init__(self, message=HTTPStatus.UNAUTHORIZED.phrase, code=""):
        super().__init__(HTTPStatus.UNAUTHORIZED.value, message, code)


class UsuarioNotFoundError(APIError):
    def __init__(self, message=HTTPStatus.NOT_FOUND.phrase):
        super().__init__(HTTPStatus.NOT_FOUND.value, message, "login.user.not_found")


class BadRequestError(APIError):
    def __init__(self, message=HTTPStatus.BAD_REQUEST.phrase, code=""):
        super().__init__(HTTPStatus.BAD_REQUEST.value, message, code)