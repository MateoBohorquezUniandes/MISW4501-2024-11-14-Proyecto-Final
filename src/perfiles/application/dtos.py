from dataclasses import dataclass, field
import datetime

from seedwork.application.dtos import DTO


@dataclass(frozen=True)
class ResultadoElementoSanguineoDTO(DTO):
    tipo_examen: str = field(default_factory=str)
    valor: float = field(default_factory=float)
    unidad: str = field(default_factory=str)


@dataclass(frozen=True)
class ReporteSanguineoDTO(DTO):
    resultado: ResultadoElementoSanguineoDTO = field(
        default_factory=ResultadoElementoSanguineoDTO
    )


@dataclass(frozen=True)
class InformacionDemograficaDTO(DTO):
    pais: str = field(default_factory=str)
    ciudad: str = field(default_factory=str)


@dataclass(frozen=True)
class InformacionFisiologicaDTO(DTO):
    genero: str = field(default_factory=str)
    edad: int = field(default_factory=int)
    altura: float = field(default_factory=float)
    peso: float = field(default_factory=float)


@dataclass(frozen=True)
class IndiceMasaCorporalDTO(DTO):
    valor: float = field(default_factory=float)
    categoria: str = field(default_factory=str)


@dataclass(frozen=True)
class VolumenMaximoOxigenoDTO(DTO):
    valor: float = field(default_factory=float)
    categoria: str = field(default_factory=str)


@dataclass(frozen=True)
class ClasificacionRiesgoDTO(DTO):
    imc: IndiceMasaCorporalDTO = field(default_factory=IndiceMasaCorporalDTO)
    vo_max: VolumenMaximoOxigenoDTO = field(default_factory=VolumenMaximoOxigenoDTO)
    riesgo: str = field(default_factory=str)


@dataclass(frozen=True)
class PerfilDemograficoDTO(DTO):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)

    clasificacion_riesgo: ClasificacionRiesgoDTO = field(
        default_factory=ClasificacionRiesgoDTO
    )
    reportes_sanguineo: list[ReporteSanguineoDTO] = field(
        default_factory=list[ReporteSanguineoDTO]
    )
    demografia: InformacionDemograficaDTO = field(
        default_factory=InformacionDemograficaDTO
    )
    fisiologia: InformacionFisiologicaDTO = field(
        default_factory=InformacionFisiologicaDTO
    )
    deportes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class HabitoDeportivoDTO(DTO):
    titulo: str = field(default_factory=str)
    frecuencia: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)


@dataclass(frozen=True)
class MolestiaDTO(DTO):
    titulo: str = field(default_factory=str)
    tipo: str = field(default_factory=str)
    fecha: str = field(default_factory=datetime)
    descripcion: str = field(default_factory=str)
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)


@dataclass(frozen=True)
class PerfilDeportivoDTO(DTO):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
    habitos: list[HabitoDeportivoDTO] = field(default_factory=list[HabitoDeportivoDTO])
    molestias: list[MolestiaDTO] = field(default_factory=list[MolestiaDTO])


@dataclass(frozen=True)
class AlimentoDTO(DTO):
    id: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    categoria: str = field(default_factory=str)
    tipo: str = field(default_factory=str)


@dataclass(frozen=True)
class PerfilAlimenticioDTO(DTO):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
    tipo_alimentacion: str = field(default_factory=str)
    alimentos: list[AlimentoDTO] = field(default_factory=list)
