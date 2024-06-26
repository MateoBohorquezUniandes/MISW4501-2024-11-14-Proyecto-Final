from seedwork.infrastructure.schema.v1.mappers import IntegrationMapper
from sesiones.domain.events import SesionEnded
from sesiones.infrastructure.schema.commands import (
    SesionEndedIntegrationEvent,
    SesionEndedPayload,
)


class SesionEndedIntegrationEventMapper(IntegrationMapper):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def external_to_message(self, external: SesionEnded) -> SesionEndedIntegrationEvent:
        payload = SesionEndedPayload(
            external.tipo_identificacion,
            external.identificacion,
            str(external.id),
            external.parametros,
        )
        return SesionEndedIntegrationEvent(
            str(external.correlation_id),
            type="command",
            datacontenttype="application/json",
            specversion="v1",
            payload=payload,
        )
