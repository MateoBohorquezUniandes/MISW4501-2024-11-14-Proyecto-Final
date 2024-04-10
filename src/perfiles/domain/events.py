import datetime
from dataclasses import dataclass, field

from seedwork.domain.events import DomainEvent


@dataclass
class PerfilDemograficoCreated(DomainEvent):
    tipo_identificacion: str = None
    identificacion: str = None
    created_at: datetime = None

    clasificacion_riesgo: dict = None
    demografia: dict = None
    fisiologia: dict = None
    deportes: list[str] = None
