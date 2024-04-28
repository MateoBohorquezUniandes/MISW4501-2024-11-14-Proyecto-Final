from seedwork.domain.exceptions import FactoryException


class InvalidIndicadorFactoryException(FactoryException):
    def __init__(self):
        super().__init__(code="factory.indice")
