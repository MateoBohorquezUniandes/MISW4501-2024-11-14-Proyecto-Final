from http import HTTPStatus


__author__ = "Santiago Cortés Fernández"
__email__ = "s.cortes@uniandes.edu.co"


class PresentationException(Exception): ...


class APIError(PresentationException):

    __status: int
    __message: str
    __code: str

    def __init__(
        self,
        status=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
        code="",
    ):
        self.__status = status
        self.__message = message
        self.__code = code

    def __str__(self) -> str:
        return self.__message

    @property
    def status(self):
        return self.__status

    @property
    def code(self):
        return self.__code
