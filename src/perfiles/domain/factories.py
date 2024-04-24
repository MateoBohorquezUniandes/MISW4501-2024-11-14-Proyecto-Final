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
    def create(self, obj: any, mapper: Mapper = None, **kwargs) -> PerfilDemografico:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj, **kwargs)

        perfil: PerfilDemografico = mapper.dto_to_entity(obj, **kwargs)
        self.validate_rule(ValidPerfilDemografico(perfil))

        return perfil


@dataclass
class _PerfilDeportivoFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None, **kwargs) -> PerfilDeportivo:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj, **kwargs)
        elif isinstance(mapper, UnidirectionalMapper):
            return mapper.map(obj, **kwargs)

        perfil: PerfilDeportivo = mapper.dto_to_entity(obj, **kwargs)
        # self.validate_rule(ValidPerfilDeportivo(perfil))

        return perfil


@dataclass
class _PerfilAlimenticioFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None, **kwargs) -> PerfilAlimenticio:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj, **kwargs)
        elif isinstance(mapper, UnidirectionalMapper):
            return mapper.map(obj, **kwargs)

        perfil: PerfilAlimenticio = mapper.dto_to_entity(obj, **kwargs)
        # self.validate_rule(ValidPerfilAlimenticio(perfil))

        return perfil


@dataclass
class _HabitoDeportivoFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None, **kwargs) -> HabitoDeportivo:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj, **kwargs)
        habito: HabitoDeportivo = mapper.dto_to_entity(obj, **kwargs)
        self.validate_rule(ValidHabitoDeportivo(habito))

        return habito


@dataclass
class _MolestiaFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None, **kwargs) -> Molestia:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj, **kwargs)
        molestia: Molestia = mapper.dto_to_entity(obj, **kwargs)
        self.validate_rule(ValidMolestia(molestia))

        return molestia


@dataclass
class PerfilFactory(Factory):
    def create(self, obj: any, mapper: Mapper, **kwargs):
        if mapper.type() == PerfilDemografico:
            perfil_factory = _PerfilDemograficoFactory()
            return perfil_factory.create(obj, mapper, **kwargs)
        elif mapper.type() == PerfilDeportivo:
            perfil_factory = _PerfilDeportivoFactory()
            return perfil_factory.create(obj, mapper, **kwargs)
        elif mapper.type() == PerfilAlimenticio:
            perfil_factory = _PerfilAlimenticioFactory()
            return perfil_factory.create(obj, mapper, **kwargs)
        elif mapper.type() == HabitoDeportivo:
            perfil_factory = _HabitoDeportivoFactory()
            return perfil_factory.create(obj, mapper, **kwargs)
        elif mapper.type() == Molestia:
            perfil_factory = _MolestiaFactory()
            return perfil_factory.create(obj, mapper, **kwargs)
        else:
            raise InvalidPerfilDemograficoFactoryException()
