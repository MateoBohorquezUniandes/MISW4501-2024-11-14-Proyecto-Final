from seedwork.infrastructure.schema.v1.mappers import IntegrationMapper
from usuarios.domain.events import UsuarioCreated
from usuarios.infrastructure.schema.v1.events import (
    DemografiaPayload,
    UsuarioCreatedIntegrationEvent,
    UsuarioCreatedPayload,
)


class UsuarioCreatedIntegrationEventMapper(IntegrationMapper):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def external_to_message(
        self, external: UsuarioCreated
    ) -> UsuarioCreatedIntegrationEvent:
        demografia: DemografiaPayload = DemografiaPayload(
            pais_nacimiento=external.demografia.get("pais_nacimiento"),
            ciudad_nacimiento=external.demografia.get("ciudad_nacimiento"),
            pais_residencia=external.demografia.get("pais_residencia"),
            ciudad_residencia=external.demografia.get("ciudad_residencia"),
            tiempo_residencia=external.demografia.get("tiempo_residencia"),
            genero=external.demografia.get("genero"),
            edad=int(external.demografia.get("edad")),
            peso=float(external.demografia.get("peso")),
            altura=float(external.demografia.get("altura")),
        )

        payload: UsuarioCreatedPayload = UsuarioCreatedPayload(
            id_usuario=str(external.id_usuario),
            created_at=external.created_at.strftime(self.DATE_FORMAT),
            demografia=demografia,
            deportes=external.deportes,
        )
        return UsuarioCreatedIntegrationEvent(
            correlation_id=str(external.correlation_id),
            type="event",
            datacontenttype="application/json",
            specversion="v1",
            payload=payload,
        )
