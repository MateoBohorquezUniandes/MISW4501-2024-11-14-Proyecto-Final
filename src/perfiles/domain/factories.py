from dataclasses import dataclass

from perfiles.domain.entities import (
    HabitoDeportivo,
    PerfilAlimenticio,
    PerfilDemografico,
    PerfilDeportivo,
    Molestia,
)
from perfiles.domain.exceptions import InvalidPerfilDemograficoFactoryException
from perfiles.domain.rules import (
    ValidHabitoDeportivo,
    ValidPerfilDemografico,
    ValidMolestia,
)
from seedwork.domain.entities import Entity
from seedwork.domain.events import DomainEvent
from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Mapper, UnidirectionalMapper


@dataclass
class _PerfilDemograficoFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None) -> PerfilDemografico:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)

        perfil: PerfilDemografico = mapper.dto_to_entity(obj)
        self.validate_rule(ValidPerfilDemografico(perfil))

        return perfil


@dataclass
class _PerfilDeportivoFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None) -> PerfilDeportivo:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)
        elif isinstance(mapper, UnidirectionalMapper):
            return mapper.map(obj)

        perfil: PerfilDeportivo = mapper.dto_to_entity(obj)
        # self.validate_rule(ValidPerfilDeportivo(perfil))

        return perfil


@dataclass
class _PerfilAlimenticioFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None) -> PerfilAlimenticio:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)
        elif isinstance(mapper, UnidirectionalMapper):
            return mapper.map(obj)

        perfil: PerfilAlimenticio = mapper.dto_to_entity(obj)
        # self.validate_rule(ValidPerfilAlimenticio(perfil))

        return perfil


@dataclass
class _HabitoDeportivoFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None) -> HabitoDeportivo:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)
        habito: HabitoDeportivo = mapper.dto_to_entity(obj)
        self.validate_rule(ValidHabitoDeportivo(habito))

        return habito


@dataclass
class _MolestiaFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None) -> Molestia:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)
        molestia: Molestia = mapper.dto_to_entity(obj)
        self.validate_rule(ValidMolestia(molestia))

        return molestia


@dataclass
class PerfilFactory(Factory):
    def create(self, obj: any, mapper: Mapper):
        if mapper.type() == PerfilDemografico:
            perfil_factory = _PerfilDemograficoFactory()
            return perfil_factory.create(obj, mapper)
        elif mapper.type() == PerfilDeportivo:
            perfil_factory = _PerfilDeportivoFactory()
            return perfil_factory.create(obj, mapper)
        elif mapper.type() == PerfilAlimenticio:
            perfil_factory = _PerfilAlimenticioFactory()
            return perfil_factory.create(obj, mapper)
        elif mapper.type() == HabitoDeportivo:
            perfil_factory = _HabitoDeportivoFactory()
            return perfil_factory.create(obj, mapper)
        elif mapper.type() == Molestia:
            perfil_factory = _MolestiaFactory()
            return perfil_factory.create(obj, mapper)
        else:
            raise InvalidPerfilDemograficoFactoryException()
