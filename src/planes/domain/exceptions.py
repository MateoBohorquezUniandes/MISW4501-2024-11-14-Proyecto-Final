from seedwork.domain.exceptions import FactoryException


class InvalidPlanesFactoryException(FactoryException):
    def __init__(self):
        super().__init__(code="factory.planes")
