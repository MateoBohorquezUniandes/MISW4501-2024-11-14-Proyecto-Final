from seedwork.domain.exceptions import DomainException, FactoryException


class InvalidUsuarioFactoryException(FactoryException):
    def __init__(self, mensaje="invalid type for factory"):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)


class InvalidPasswordFactoryException(FactoryException):
    def __init__(self, mensaje="invalid type for factory"):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)

class InvalidLoginFactoryException(FactoryException):
    def __init__(self, mensaje="invalid type for factory"):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)


class InvalidPasswordMatchError(DomainException):
    def __init__(self, mensaje="invalid credentials"):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)