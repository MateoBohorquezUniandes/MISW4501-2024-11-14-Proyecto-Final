import uuid
from dataclasses import dataclass, field

import planes.domain.value_objects as vo
import seedwork.domain.value_objects as svo
from planes.domain.events import (
    EntrenamientoCreated,
    PlanEntrenamientoCreated,
    UsuarioPlanCreated,
)
from seedwork.domain.entities import Entity, RootAggregation


@dataclass
class Entrenamiento(RootAggregation):
    nombre: str = field(default_factory=str)

    grupo_muscular: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    imagen: vo.Imagen = field(default_factory=vo.Imagen)

    duracion: vo.Duracion = field(default_factory=vo.Duracion)

    def create(self, correlation_id: uuid.UUID):
        self.events.append(
            EntrenamientoCreated(
                id=self.id,
                correlation_id=correlation_id,
                nombre=self.nombre,
                created_at=self.created_at,
            )
        )


@dataclass
class PlanEntrenamiento(RootAggregation):
    nombre: str = field(default_factory=str)
    categoria: vo.PLAN_CATEGORIA = field(default="")
    descripcion: str = field(default_factory=str)
    objetivo: vo.ObjetivoEntrenamiento = field(default_factory=vo.ObjetivoEntrenamiento)

    entrenamientos: list[Entrenamiento] = field(default_factory=list)

    def create(self, correlation_id: uuid.UUID):
        self.events.append(
            PlanEntrenamientoCreated(
                id=self.id,
                correlation_id=correlation_id,
                nombre=self.nombre,
                created_at=self.created_at,
            )
        )


@dataclass
class UsuarioPlan(RootAggregation):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
    planes_entrenamiento: list[PlanEntrenamiento] = field(default_factory=list)

    def create(self, correlation_id: uuid.UUID):
        self.events.append(
            UsuarioPlanCreated(
                correlation_id=correlation_id,
                tipo_identificacion=self.tipo_identificacion,
                identificacion=self.identificacion,
                created_at=self.created_at,
            )
        )


@dataclass
class RutinaRecuperacion(Entity):
    nombre: str = field(default_factory=str)

    tipo: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    imagen: vo.Imagen = field(default_factory=vo.Imagen)

    deporte: vo.DEPORTE = field(default_factory=str)
    frecuencia: vo.Frecuencia = field(default_factory=vo.Frecuencia)


@dataclass
class GrupoAlimenticio(Entity):
    grupo: svo.CATEGORIA_ALIMENTO = field(default="")
    porcion: float = field(default_factory=float)
    unidad: vo.PORCION_UNIDAD = field(default="")
    calorias: float = field(default_factory=float)


@dataclass
class RutinaAlimentacion(RootAggregation):
    nombre: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    imagen: str = field(default_factory=str)

    tipo_alimentacion: svo.TIPO_ALIMENTACION = field(default_factory=str)
    deporte: svo.DEPORTE = field(default_factory=str)

    grupos_alimenticios: list[GrupoAlimenticio] = field(default_factory=list)
