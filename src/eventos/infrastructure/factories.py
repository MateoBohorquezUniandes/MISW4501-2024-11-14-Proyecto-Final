from dataclasses import dataclass
from eventos.domain.entities import Evento
from eventos.domain.value_objects import EventoAsociado
from eventos.infrastructure.repositories import EventoAsociadoRepositoryPostgreSQL, EventoRepositoryPostgreSQL
from eventos.infrastructure.exceptions import InvalidRepositoryFactoryException

from seedwork.domain.factories import Factory


@dataclass
class RepositoryFactory(Factory):
    def create(self, obj):
        if isinstance(obj, Evento) or obj == Evento:
            return EventoRepositoryPostgreSQL()
        elif isinstance(obj, EventoAsociado) or obj == EventoAsociado:
            return EventoAsociadoRepositoryPostgreSQL()
        else:
            raise InvalidRepositoryFactoryException()
