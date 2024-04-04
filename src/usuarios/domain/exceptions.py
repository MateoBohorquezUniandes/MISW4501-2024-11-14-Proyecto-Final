from seedwork.domain.exceptions import DomainException, FactoryException


class InvalidUsuarioFactoryException(FactoryException):
    def __init__(self):
        super().__init__(code="factory.usuario")


class InvalidPasswordFactoryException(FactoryException):
    def __init__(self):
        super().__init__(code="factory.contrasena")

class InvalidLoginFactoryException(FactoryException):
    def __init__(self):
        super().__init__(code="factory.login")


class InvalidPasswordMatchError(DomainException):
    def __init__(self, message="credenciales incorrectas"):
        super().__init__(message, code="login.credentials")
        self.__message = message

class InvalidRolUsuarioError(DomainException):
    def __init__(self, message="rol invalido"):
        super().__init__(message, code="login.credentials")
