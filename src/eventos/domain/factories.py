from dataclasses import dataclass

from eventos.domain.entities import Evento
from eventos.domain.rules import ValidEvento
from eventos.domain.exceptions import InvalidEventoFactoryException

from seedwork.domain.entities import Entity
from seedwork.domain.events import DomainEvent
from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Mapper


@dataclass
class _EventoFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None) -> Evento:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)

        evento: Evento = mapper.dto_to_entity(obj)
        self.validate_rule(ValidEvento(evento))

        return evento


@dataclass
class EventoFactoy(Factory):
    def create(self, obj: any, mapper: Mapper):
        if mapper.type() == Evento:
            evento_factory = _EventoFactory()
            return evento_factory.create(obj, mapper)
        else:
            raise InvalidEventoFactoryException()
