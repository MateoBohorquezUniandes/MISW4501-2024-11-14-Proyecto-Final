from dataclasses import dataclass, field

from seedwork.domain.value_objects import ValueObject


@dataclass(frozen=True)
class Parametro(ValueObject):
    id: str = field(default=str)
    nombre: str = field(default=str)
    simbolo: str = field(default=str)
    funcion: str = field(default=str)
