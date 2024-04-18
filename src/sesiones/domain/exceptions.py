from seedwork.domain.exceptions import FactoryException


class InvalidSesionesFactoryException(FactoryException):
    def __init__(self):
        super().__init__(code="factory.planes")
