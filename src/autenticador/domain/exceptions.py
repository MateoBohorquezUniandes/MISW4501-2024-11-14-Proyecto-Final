from seedwork.domain.exceptions import FactoryException


class InvalidTokenRequestFactoryException(FactoryException):
    def __init__(self):
        super().__init__(code="factory.token")
