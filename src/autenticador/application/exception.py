from http import HTTPStatus
from seedwork.presentation.exceptions import APIError


class UnprocessableTokenRequestError(APIError):
    def __init__(self, message=HTTPStatus.UNPROCESSABLE_ENTITY.phrase, code=""):
        super().__init__(HTTPStatus.UNPROCESSABLE_ENTITY.value, message, code)
