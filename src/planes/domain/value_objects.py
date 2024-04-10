from dataclasses import dataclass, field

from seedwork.domain.value_objects import ExtendedEnum, ValueObject


class PLAN_CATEGORIA(ExtendedEnum):
    RESISTENCIA = "Resistencia"
    FORTALECIMIENTO = "Fortalecimiento"
    EQUILIBRIO = "Equilibrio"
    FLEXIBILIDAD = "Flexibilidad"


class DEPORTE(ExtendedEnum):
    CILICMO = "Ciclismo"
    ATLETISMO = "Atletismo"


class EXIGENCIA(ExtendedEnum):
    SEDENTARIO = "Sedentario"
    PRINCIPIANTE = "Principiante"
    MODERADA = "Moderada"
    ALTA = "Alta"
    ALTO_RENDIMIENTO = "Alto rendimiento"


class DURACION_UNIDAD(ExtendedEnum):
    REPETICIONES = "reps"
    MINUTOS = "min"
    HORAS = "h"


@dataclass(frozen=True)
class ObjetivoEntrenamiento(ValueObject):
    exigencia: EXIGENCIA = field(default=EXIGENCIA.MODERADA.value)
    deporte: DEPORTE = field(default_factory=str)


@dataclass(frozen=True)
class Duracion(ValueObject):
    valor: int = field(default_factory=int)
    unidad: DURACION_UNIDAD = field(default=DURACION_UNIDAD.REPETICIONES)
    series: int = field(default_factory=int)


@dataclass(frozen=True)
class Imagen(ValueObject):
    url: str = field(default_factory=str)


@dataclass(frozen=True)
class Porcion(ValueObject):
    cantidad: float = field(default_factory=float)
    unidad: str = field(default_factory=str)
    calorias: float = field(default_factory=float)


@dataclass(frozen=True)
class Frecuencia(ValueObject):
    valor: int = field(default_factory=int)
    unidad: int = field(default_factory=int)
