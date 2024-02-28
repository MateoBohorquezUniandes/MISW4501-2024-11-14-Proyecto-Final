from http import HTTPStatus


__author__ = "Santiago Cortés Fernández"
__email__ = "s.cortes@uniandes.edu.co"


class PresentationException(Exception): ...


class APIError(PresentationException):

    status: HTTPStatus.INTERNAL_SERVER_ERROR.value
    __message: str

    def __init__(self, message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase):
        self.__message = message

    def __str__(self) -> str:
        return f"{self.status} {self.__message}"
