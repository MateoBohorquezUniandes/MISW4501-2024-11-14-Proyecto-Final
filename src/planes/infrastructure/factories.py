from dataclasses import dataclass

from planes.domain.entities import (
    Entrenamiento,
    GrupoAlimenticio,
    PlanEntrenamiento,
    RutinaAlimentacion,
    RutinaRecuperacion,
    UsuarioPlan,
)
from planes.infrastructure.exceptions import InvalidRepositoryFactoryException
from planes.infrastructure.repositories import (
    EntrenamientoRepositoryPostgreSQL,
    GrupoAlimenticioRepositoryPostgreSQL,
    PlanEntrenamientoRepositoryPostgreSQL,
    RutinaAlimentacionRepositoryPostgreSQL,
    RutinaRecuperacionRepositoryPostgreSQL,
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
        elif isinstance(obj, GrupoAlimenticio) or obj == GrupoAlimenticio:
            return GrupoAlimenticioRepositoryPostgreSQL()
        elif isinstance(obj, RutinaAlimentacion) or obj == RutinaAlimentacion:
            return RutinaAlimentacionRepositoryPostgreSQL()
        elif isinstance(obj, RutinaRecuperacion) or obj == RutinaRecuperacion:
            return RutinaRecuperacionRepositoryPostgreSQL()
        else:
            raise InvalidRepositoryFactoryException()
