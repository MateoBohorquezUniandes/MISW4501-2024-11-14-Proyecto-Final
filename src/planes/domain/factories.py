from dataclasses import dataclass

from planes.domain.entities import Entrenamiento, PlanEntrenamiento, UsuarioPlan
from planes.domain.exceptions import InvalidPlanesFactoryException
from planes.domain.rules import (
    ValidEntrenamiento,
    ValidObjetivo,
    ValidPlanEntrenamiento,
    ValidUsuarioPlan,
)
from planes.domain.value_objects import ObjetivoEntrenamiento
from seedwork.domain.entities import Entity
from seedwork.domain.events import DomainEvent
from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Mapper
from seedwork.domain.value_objects import ValueObject


@dataclass
class _EntrenamientoFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None) -> Entrenamiento:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)

        entrenamiento: Entrenamiento = mapper.dto_to_entity(obj)
        self.validate_rule(ValidEntrenamiento(entrenamiento))

        return entrenamiento


@dataclass
class _ObjetivoEntrenamientoFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None) -> ObjetivoEntrenamiento:
        if isinstance(obj, ValueObject):
            return mapper.entity_to_dto(obj)

        objetivo: ObjetivoEntrenamiento = mapper.dto_to_entity(obj)
        self.validate_rule(ValidObjetivo(objetivo))

        return objetivo


@dataclass
class _PlanEntrenamientoFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None) -> PlanEntrenamiento:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)

        plan: PlanEntrenamiento = mapper.dto_to_entity(obj)
        self.validate_rule(ValidPlanEntrenamiento(plan))

        return plan


@dataclass
class _UsuarioPlanFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None) -> UsuarioPlan:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)

        usuario: UsuarioPlan = mapper.dto_to_entity(obj)
        self.validate_rule(ValidUsuarioPlan(usuario))

        return usuario


@dataclass
class PlanFactory(Factory):
    def create(self, obj: any, mapper: Mapper):
        if mapper.type() == Entrenamiento:
            entrenamiento_factory = _EntrenamientoFactory()
            return entrenamiento_factory.create(obj, mapper)
        elif mapper.type() == ObjetivoEntrenamiento:
            objetivo_factory = _ObjetivoEntrenamientoFactory()
            return objetivo_factory.create(obj, mapper)
        elif mapper.type() == PlanEntrenamiento:
            plan_factory = _PlanEntrenamientoFactory()
            return plan_factory.create(obj, mapper)
        elif mapper.type() == UsuarioPlan:
            usuario_facotry = _UsuarioPlanFactory()
            return usuario_facotry.create(obj, mapper)
        else:
            raise InvalidPlanesFactoryException()
