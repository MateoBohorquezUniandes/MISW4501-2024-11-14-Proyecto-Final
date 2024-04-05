from seedwork.infrastructure.schema.v1.mappers import IntegrationMapper
from perfiles.domain.events import PerfilDemograficoCreated
from perfiles.infrastructure.schema.v1.events import (
    ClasificacionRiesgoPayload,
    DemografiaCreatedPayload,
    DemograficaCreatedIntegrationEvent,
    IndiceMasaCorporalPayload,
    InformacionDemograficaPayload,
    InformacionFisiologicaPayload,
)


class DemografiaCreatedIntegrationEventMapper(IntegrationMapper):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def external_to_message(
        self, external: PerfilDemograficoCreated
    ) -> DemograficaCreatedIntegrationEvent:
        imc = external.clasificacion_riesgo.get("imc", {})
        clasificacion = ClasificacionRiesgoPayload(
            imc=IndiceMasaCorporalPayload(imc.getr("valor"), imc.getr("categoria")),
            riesgo=external.clasificacion_riesgo.get("riesgo"),
        )

        demografia = InformacionDemograficaPayload(
            external.demografia.get("pais"),
            external.demografia.get("ciudad"),
        )

        fisiologia = InformacionFisiologicaPayload(
            external.fisiologia.get("genero"),
            int(external.fisiologia.get("edad")),
            float(external.fisiologia.get("altura")),
            float(external.fisiologia.get("peso")),
        )

        payload: DemografiaCreatedPayload = DemografiaCreatedPayload(
            tipo_identificacion=str(external.tipo_identificacion),
            identificacion=str(external.identificacion),
            created_at=external.created_at.strftime(self.DATE_FORMAT),
            clasificacion_riesgo=clasificacion,
            demografia=demografia,
            fisiologia=fisiologia,
        )
        return DemograficaCreatedIntegrationEvent(
            correlation_id=str(external.correlation_id),
            type="event",
            datacontenttype="application/json",
            specversion="v1",
            payload=payload,
        )
