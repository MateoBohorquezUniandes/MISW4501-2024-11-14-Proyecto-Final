from dataclasses import dataclass

from seedwork.domain.factories import Factory
from sesiones.domain.entities import SesionDeportiva
from sesiones.infrastructure.exceptions import InvalidRepositoryFactoryException
from sesiones.infrastructure.repositories import SesionDeportivaRepositoryPostgreSQL


@dataclass
class RepositoryFactory(Factory):
    def create(self, obj):
        if isinstance(obj, SesionDeportiva) or obj == SesionDeportiva:
            return SesionDeportivaRepositoryPostgreSQL()
        else:
            raise InvalidRepositoryFactoryException()
