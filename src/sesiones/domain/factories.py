

from dataclasses import dataclass

from seedwork.application.dtos import Mapper
from seedwork.domain.entities import Entity
from seedwork.domain.events import DomainEvent
from seedwork.domain.factories import Factory
from sesiones.domain.entities import SesionDeportiva
from sesiones.domain.exceptions import InvalidSesionesFactoryException
from sesiones.domain.rules import ValidSesionDeportiva


@dataclass
class _SesionDeportivaFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None) -> SesionDeportiva:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)

        sesion: SesionDeportiva = mapper.dto_to_entity(obj)
        self.validate_rule(ValidSesionDeportiva(sesion))

        return sesion


@dataclass
class SesionFactory(Factory):
    def create(self, obj: any, mapper: Mapper):
        if mapper.type() == SesionDeportiva:
            perfil_factory = _SesionDeportivaFactory()
            return perfil_factory.create(obj, mapper)
        else:
            raise InvalidSesionesFactoryException()