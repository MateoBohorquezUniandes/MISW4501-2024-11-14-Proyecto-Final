from dataclasses import dataclass, field, asdict
import uuid
from seedwork.domain.entities import Entity, RootAggregation
import perfiles.domain.value_objects as vo
from perfiles.domain.events import PerfilDemograficoCreated


@dataclass
class ReporteSanguineo(Entity):
    resultado: vo.ResultadoElementoSanguineo = field(
        default_factory=vo.ResultadoElementoSanguineo
    )


@dataclass
class PerfilDemografico(RootAggregation):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)

    clasificacion_riesgo: vo.ClasificacionRiesgo = field(
        default_factory=vo.ClasificacionRiesgo
    )

    reportes_sanguineo: list[ReporteSanguineo] = field(
        default_factory=list
    )
    demografia: vo.InformacionDemografica = field(
        default_factory=vo.InformacionDemografica
    )
    fisiologia: vo.InformacionFisiologica = field(
        default_factory=vo.InformacionFisiologica
    )

    def create(self, correlation_id: uuid.UUID, deportes: list[str] = []):
        self.append_event(
            PerfilDemograficoCreated(
                correlation_id=correlation_id,
                tipo_identificacion=self.tipo_identificacion,
                identificacion=self.identificacion,
                created_at=self.created_at,
                clasificacion_riesgo=asdict(self.clasificacion_riesgo),
                demografia=asdict(self.demografia),
                fisiologia=asdict(self.fisiologia),
                deportes=deportes,
            )
        )


@dataclass
class PerfilDeportivo(RootAggregation):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)


@dataclass
class PerfilAlimenticio(RootAggregation):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)

@dataclass
class HabitoDeportivo(RootAggregation):
    titulo: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    frecuencia: vo.HabitoDeportivoFrecuencia = field(
        default_factory=vo.HabitoDeportivoFrecuencia
    )
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
