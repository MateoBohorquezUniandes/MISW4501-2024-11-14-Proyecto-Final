from dataclasses import dataclass, field

from seedwork.domain.value_objects import ValueObject


@dataclass(frozen=True)
class Objetivo(ValueObject):
    exigencia: str = field(default=str)
    deporte: str = field(default=str)

VO_MAX_KEY = "vo2max"