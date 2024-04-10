from dataclasses import dataclass

from planes.domain.entities import Entrenamiento, PlanEntrenamiento, UsuarioPlan

from planes.infrastructure.exceptions import InvalidRepositoryFactoryException
from planes.infrastructure.repositories import (
    EntrenamientoRepositoryPostgreSQL,
    PlanEntrenamientoRepositoryPostgreSQL,
    UsuarioPlanRepositoryPostgreSQL,
)
from seedwork.domain.factories import Factory


@dataclass
class RepositoryFactory(Factory):
    def create(self, obj):
        if isinstance(obj, Entrenamiento) or obj == Entrenamiento:
            return EntrenamientoRepositoryPostgreSQL()
        elif isinstance(obj, PlanEntrenamiento) or obj == PlanEntrenamiento:
            return PlanEntrenamientoRepositoryPostgreSQL()
        elif isinstance(obj, UsuarioPlan) or obj == UsuarioPlan:
            return UsuarioPlanRepositoryPostgreSQL()
        else:
            raise InvalidRepositoryFactoryException()
