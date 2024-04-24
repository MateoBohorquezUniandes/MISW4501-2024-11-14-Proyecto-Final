from dataclasses import dataclass, field

from seedwork.infrastructure.schema.v1.events import IntegrationEvent
from seedwork.infrastructure.schema.v1.messages import MessagePayload


@dataclass(frozen=True)
class InformacionFisiologicaPayload(MessagePayload):
    genero: str = field(default_factory=str)
    edad: int = field(default_factory=int)
    altura: float = field(default_factory=float)
    peso: float = field(default_factory=float)


@dataclass(frozen=True)
class InformacionDemograficaPayload(MessagePayload):
    pais: str = field(default_factory=str)
    ciudad: str = field(default_factory=str)


@dataclass(frozen=True)
class IndiceMasaCorporalPayload(MessagePayload):
    valor: float = field(default_factory=float)
    categoria: str = field(default_factory=str)


@dataclass(frozen=True)
class VolumenMaximoOxigenoPayload(MessagePayload):
    valor: float = field(default_factory=float)
    categoria: str = field(default_factory=str)


@dataclass(frozen=True)
class ClasificacionRiesgoPayload(MessagePayload):
    imc: IndiceMasaCorporalPayload = field(default_factory=IndiceMasaCorporalPayload)
    vo_max: VolumenMaximoOxigenoPayload = field(
        default_factory=VolumenMaximoOxigenoPayload
    )
    riesgo: str = field(default_factory=str)


@dataclass(frozen=True)
class DemograficoModifiedPayload(MessagePayload):
    created_at: str = field(default_factory=str)
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)

    clasificacion_riesgo: ClasificacionRiesgoPayload = field(
        default_factory=ClasificacionRiesgoPayload
    )
    demografia: InformacionDemograficaPayload = field(
        default_factory=InformacionDemograficaPayload
    )
    fisiologia: InformacionFisiologicaPayload = field(
        default_factory=InformacionFisiologicaPayload
    )
    deportes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class DemograficoModifiedIntegrationEvent(IntegrationEvent):
    payload: DemograficoModifiedPayload = field(
        default_factory=DemograficoModifiedPayload
    )
