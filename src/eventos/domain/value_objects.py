from dataclasses import dataclass, field
from enum import Enum

from seedwork.domain.value_objects import DEPORTE, ExtendedEnum, ValueObject


class EXIGENCIA(ExtendedEnum):
    SEDENTARIO = "Sedentario"
    PRINCIPIANTE = "Principiante"
    MODERADA = "Moderada"
    ALTA = "Alta"
    ALTO_RENDIMIENTO = "Alto rendimiento"


@dataclass(frozen=True)
class EventoTipo(ValueObject):
    tipo: DEPORTE = field(default_factory=DEPORTE)


@dataclass(frozen=True)
class EventoNivel(ValueObject):
    nivel: EXIGENCIA = field(default_factory=EXIGENCIA)

@dataclass(frozen=True)
class EventoAsociado(ValueObject):
    id: str = field(default_factory=str)
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
    fecha: str = field(default_factory=str)
