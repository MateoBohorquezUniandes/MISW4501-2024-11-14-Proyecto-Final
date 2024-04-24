from dataclasses import dataclass

from seedwork.domain.events import DomainEvent


@dataclass
class SesionEnded(DomainEvent):
    parametros: dict = None
