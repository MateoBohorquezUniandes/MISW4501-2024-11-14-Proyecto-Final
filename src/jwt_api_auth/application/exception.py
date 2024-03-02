from seedwork.domain.exceptions import FactoryException


class UserNotFoundException(FactoryException):
    def __init__(self, mensaje="user not found"):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)
    
class WrongPasswordException(FactoryException):
    def __init__(self, mensaje="wrong password"):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)