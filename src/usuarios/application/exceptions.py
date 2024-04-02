from http import HTTPStatus
from seedwork.presentation.exceptions import APIError


class UnprocessableEntityError(APIError):

    status: HTTPStatus.UNPROCESSABLE_ENTITY.value
    __message: str

    def __init__(self, message=HTTPStatus.UNPROCESSABLE_ENTITY.phrase):
        self.__message = message

    def __str__(self) -> str:
        return f"{self.status} {self.__message}"

class InvalidCredentialsError(APIError):

    status: HTTPStatus.UNAUTHORIZED.value
    __message: str

    def __init__(self, message=HTTPStatus.UNAUTHORIZED.phrase):
        self.__message = message

    def __str__(self) -> str:
        return f"{self.status} {self.__message}"