from seedwork.domain.exceptions import DomainException, FactoryException


class InvalidPerfilDemograficoFactoryException(FactoryException):
    def __init__(self):
        super().__init__(code="factory.usuario")
