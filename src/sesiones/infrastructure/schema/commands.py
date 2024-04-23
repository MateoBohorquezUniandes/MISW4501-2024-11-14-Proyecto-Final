from dataclasses import dataclass, field

from seedwork.infrastructure.schema.v1.commands import IntegrationCommand
from seedwork.infrastructure.schema.v1.messages import MessagePayload


@dataclass(frozen=True)
class SesionEndedPayload(MessagePayload):
    parametros: dict = field(default_factory=dict)


@dataclass(frozen=True)
class SesionEndedIntegrationEvent(IntegrationCommand):
    payload: SesionEndedPayload = field(default_factory=SesionEndedPayload)