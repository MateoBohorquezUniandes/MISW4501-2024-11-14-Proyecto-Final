from seedwork.domain.exceptions import DomainException, FactoryException


class InvalidEventoFactoryException(FactoryException):
    def __init__(self):
        super().__init__(code="factory.evento")
