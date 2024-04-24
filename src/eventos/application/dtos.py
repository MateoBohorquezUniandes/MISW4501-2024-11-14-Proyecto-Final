from dataclasses import dataclass, field
import datetime

from seedwork.application.dtos import DTO


@dataclass(frozen=True)
class EventoDTO(DTO):
    id: str = field(default_factory=str)
    tipo: str = field(default_factory=str)
    fecha: str = field(default_factory=datetime)
    lugar: str = field(default_factory=str)
    distancia: float = field(default_factory=float)
    nivel: str = field(default_factory=str)
