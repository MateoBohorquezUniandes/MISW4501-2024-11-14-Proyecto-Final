from dataclasses import dataclass, field
import uuid
from seedwork.domain.entities import Entity, RootAggregation
import perfiles.domain.value_objects as vo


@dataclass
class ReporteSanguineo(Entity):
    resultados: vo.ResultadoElementoSanguineo = field(
        default_factory=vo.ResultadoElementoSanguineo
    )


@dataclass
class PerfilDemografico(RootAggregation):
    id_usuario: uuid.UUID = field(hash=True, default=None)
    clasificacion_riesgo: vo.ClasificacionRiesgo = field(
        default_factory=vo.ClasificacionRiesgo
    )

    reporte_sanguineo: list[ReporteSanguineo] = field(
        default_factory=list[ReporteSanguineo]
    )
    reporte_demografico: vo.InformacionDemografica = field(
        default_factory= vo.InformacionDemografica
    )
    fisiologia: vo.InformacionFisiologica = field(
        default_factory= vo.InformacionFisiologica
    )
    


@dataclass
class HabitoDeportivo(Entity):
    tipo: vo.TipoActividadDeportiva = field(default_factory=vo.TipoActividadDeportiva)
    frecuencia: vo.FrecuenciaActividadDeportiva = field(
        default_factory=vo.FrecuenciaActividadDeportiva
    )


@dataclass
class PerfilDeportivo(RootAggregation):
    id_usuario: uuid.UUID = field(hash=True, default=None)
    habitos: list[HabitoDeportivo] = field(default_factory=list[HabitoDeportivo])
    # lesiones: list
    # incapacidades: list


@dataclass
class PerfilAlimenticio(RootAggregation):
    id_usuario: uuid.UUID = field(hash=True, default=None)
    tipo_alimentacion: vo.TipoAlimentacion = field(default_factory=vo.TipoAlimentacion)
    # preferencias: list
    # limitaciones: list
