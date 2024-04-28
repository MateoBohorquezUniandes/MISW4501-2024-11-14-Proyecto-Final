from dataclasses import dataclass, field

from seedwork.domain.value_objects import ValueObject


@dataclass(frozen=True)
class Objetivo(ValueObject):
    exigencia: str = field(default=str)
    deporte: str = field(default=str)


@dataclass(frozen=True)
class Indicadores(ValueObject):
    nombre: str = field(default=str)
    valor: float = field(default=float)
    varianza: float = field(default=float)
