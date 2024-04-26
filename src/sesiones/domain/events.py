from dataclasses import dataclass

from seedwork.domain.events import DomainEvent


@dataclass
class SesionEnded(DomainEvent):
    tipo_identificacion: str = None
    identificacion: str = None
    parametros: dict = None
    vo_max: float = None
