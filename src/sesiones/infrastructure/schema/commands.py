from dataclasses import dataclass, field

from seedwork.infrastructure.schema.v1.commands import IntegrationCommand
from seedwork.infrastructure.schema.v1.messages import MessagePayload


@dataclass(frozen=True)
class SesionEndedPayload(MessagePayload):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
    id: str = field(default_factory=str)
    parametros: dict = field(default_factory=dict)
    vo_max: float = field(default_factory=float)


@dataclass(frozen=True)
class SesionEndedIntegrationEvent(IntegrationCommand):
    payload: SesionEndedPayload = field(default_factory=SesionEndedPayload)
