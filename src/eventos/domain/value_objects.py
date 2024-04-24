from dataclasses import dataclass, field
from enum import Enum

from seedwork.domain.value_objects import ExtendedEnum, ValueObject


class EXIGENCIA(ExtendedEnum):
    SEDENTARIO = "Sedentario"
    PRINCIPIANTE = "Principiante"
    MODERADA = "Moderada"
    ALTA = "Alta"
    ALTO_RENDIMIENTO = "Alto rendimiento"


class EventoTipoEnum(str, ExtendedEnum):
    CICLISMO = "ciclismo"
    ATLETISMO = "Atletismo"


@dataclass(frozen=True)
class EventoTipo(ValueObject):
    tipo: EventoTipoEnum = field(default_factory=EventoTipoEnum)


@dataclass(frozen=True)
class EventoNivel(ValueObject):
    nivel: EXIGENCIA = field(default_factory=EXIGENCIA)
