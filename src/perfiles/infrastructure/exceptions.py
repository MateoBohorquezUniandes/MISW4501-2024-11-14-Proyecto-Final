from seedwork.domain.exceptions import FactoryException


class InvalidRepositoryFactoryException(FactoryException):
    def __init__(self):
        super().__init__(code="factory.repository")

