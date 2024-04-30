import datetime
import uuid
from dataclasses import asdict, dataclass, field

import perfiles.domain.value_objects as vo
from perfiles.domain.events import PerfilDemograficoModified
from seedwork.domain.entities import Entity, RootAggregation


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

    reportes_sanguineo: list[ReporteSanguineo] = field(default_factory=list)
    demografia: vo.InformacionDemografica = field(
        default_factory=vo.InformacionDemografica
    )
    fisiologia: vo.InformacionFisiologica = field(
        default_factory=vo.InformacionFisiologica
    )

    def create(self, correlation_id: uuid.UUID, deportes: list[str] = []):
        self.append_event(
            PerfilDemograficoModified(
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

    def update(self, correlation_id: uuid.UUID):
        self.append_event(
            PerfilDemograficoModified(
                correlation_id=correlation_id,
                tipo_identificacion=self.tipo_identificacion,
                identificacion=self.identificacion,
                created_at=self.created_at,
                clasificacion_riesgo=asdict(self.clasificacion_riesgo),
                demografia=asdict(self.demografia),
                fisiologia=asdict(self.fisiologia),
                deportes=[],
            )
        )


@dataclass
class HabitoDeportivo(RootAggregation):
    titulo: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    frecuencia: vo.HabitoDeportivoFrecuencia = field(
        default_factory=vo.HabitoDeportivoFrecuencia
    )
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)


@dataclass
class Molestia(Entity):
    titulo: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    tipo: vo.MolestiaTipo = field(default_factory=vo.MolestiaTipo)
    fecha: str = field(default_factory=datetime)
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)


@dataclass
class PerfilDeportivo(RootAggregation):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
    habitos_deportivos: list[HabitoDeportivo] = field(default_factory=list)
    molestias: list[Molestia] = field(default_factory=list)


@dataclass
class Alimento(Entity):
    nombre: str = field(default_factory=str)
    categoria: vo.CategoriaAlimento = field(default=None)
    tipo: vo.CategoriaAsociacionAlimento = field(default=None)


@dataclass
class PerfilAlimenticio(RootAggregation):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
    alimentos: list[Alimento] = field(default_factory=list)
