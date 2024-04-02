from dataclasses import dataclass, field
import datetime

from seedwork.domain.value_objects import ValueObject


@dataclass(frozen=True)
class Identidad(ValueObject):
    tipo: str = field(default_factory=str)
    valor: str = field(default_factory=str)
