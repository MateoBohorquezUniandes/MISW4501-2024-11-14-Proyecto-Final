from perfiles.domain.events import PerfilDemograficoModified
from perfiles.infrastructure.schema.v1.events import (
    ClasificacionRiesgoPayload,
    DemograficoModifiedPayload,
    DemograficoModifiedIntegrationEvent,
    IndiceMasaCorporalPayload,
    InformacionDemograficaPayload,
    InformacionFisiologicaPayload,
    VolumenMaximoOxigenoPayload,
)
from seedwork.infrastructure.schema.v1.mappers import IntegrationMapper


class DemograficoModifiedIntegrationEventMapper(IntegrationMapper):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def external_to_message(
        self, external: PerfilDemograficoModified
    ) -> DemograficoModifiedIntegrationEvent:
        print(external.clasificacion_riesgo)
        imc = external.clasificacion_riesgo.get("imc", {})
        vom = external.clasificacion_riesgo.get("vo_max", {})
        clasificacion = ClasificacionRiesgoPayload(
            imc=IndiceMasaCorporalPayload(imc.get("valor"), imc.get("categoria")),
            vo_max=VolumenMaximoOxigenoPayload(vom.get("valor"), vom.get("categoria")),
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

        payload: DemograficoModifiedPayload = DemograficoModifiedPayload(
            tipo_identificacion=str(external.tipo_identificacion),
            identificacion=str(external.identificacion),
            created_at=external.created_at.strftime(self.DATE_FORMAT),
            clasificacion_riesgo=clasificacion,
            demografia=demografia,
            fisiologia=fisiologia,
            deportes=external.deportes,
        )
        return DemograficoModifiedIntegrationEvent(
            correlation_id=str(external.correlation_id),
            type="event",
            datacontenttype="application/json",
            specversion="v1",
            payload=payload,
        )
