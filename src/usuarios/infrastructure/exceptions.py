from seedwork.domain.exceptions import FactoryException


class InvalidRepositoryFactoryException(FactoryException):
    def __init__(self, mensaje="invalid type for repository"):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)
