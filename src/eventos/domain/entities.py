import datetime
import eventos.domain.value_objects as vo
from dataclasses import asdict, dataclass, field

from seedwork.domain.entities import Entity, RootAggregation


@dataclass
class Evento(RootAggregation):
    nombre: str = field(default_factory=str)
    tipo: vo.EventoTipo = field(default_factory=vo.EventoTipo)
    fecha: str = field(default_factory=str)
    lugar: str = field(default_factory=str)
    distancia: float = field(default_factory=float)
    nivel: vo.EventoNivel = field(default_factory=vo.EventoNivel)
