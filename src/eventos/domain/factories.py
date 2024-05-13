from dataclasses import dataclass

from eventos.domain.entities import Evento
from eventos.domain.rules import ValidEvento
from eventos.domain.exceptions import InvalidEventoFactoryException

from eventos.domain.value_objects import EventoAsociado
from seedwork.domain.entities import Entity
from seedwork.domain.events import DomainEvent
from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Mapper, UnidirectionalMapper
from seedwork.domain.value_objects import ValueObject


@dataclass
class _EventoFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None) -> Evento:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)

        evento: Evento = mapper.dto_to_entity(obj)
        self.validate_rule(ValidEvento(evento))

        return evento


@dataclass
class _EventoAsociadoFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None, **kwargs) -> EventoAsociado:
        if isinstance(mapper, UnidirectionalMapper):
            return mapper.map(obj, **kwargs)
        elif isinstance(obj, ValueObject):
            return mapper.entity_to_dto(obj, **kwargs)
        asociacion: EventoAsociado = mapper.dto_to_entity(obj, **kwargs)

        return asociacion


@dataclass
class EventoFactoy(Factory):
    def create(self, obj: any, mapper: Mapper, **kwargs):
        if mapper.type() == Evento:
            evento_factory = _EventoFactory()
            return evento_factory.create(obj, mapper)
        elif mapper.type() == EventoAsociado:
            asociacion_factory = _EventoAsociadoFactory()
            return asociacion_factory.create(obj, mapper, **kwargs)
        else:
            raise InvalidEventoFactoryException()
