from dataclasses import dataclass
from eventos.domain.entities import Evento
from eventos.infrastructure.repositories import EventoRepositoryPostgreSQL
from eventos.infrastructure.exceptions import InvalidRepositoryFactoryException

from seedwork.domain.factories import Factory


@dataclass
class RepositoryFactory(Factory):
    def create(self, obj):
        if isinstance(obj, Evento) or obj == Evento:
            return EventoRepositoryPostgreSQL()

        else:
            raise InvalidRepositoryFactoryException()
