from dataclasses import dataclass, field

from seedwork.application.dtos import DTO


@dataclass(frozen=True)
class DuracionDTO(DTO):
    valor: int = field(default_factory=int)
    unidad: str = field(default_factory=str)
    series: int = field(default_factory=int)


@dataclass(frozen=True)
class EntrenamientoDTO(DTO):
    created_at: str = field(default_factory=str)
    updated_at: str = field(default_factory=str)
    id: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    grupo_muscular: str = field(default_factory=str)
    imagen: str = field(default_factory=str)
    duracion: DuracionDTO = field(default_factory=DuracionDTO)


@dataclass(frozen=True)
class ObjetivoEntrenamientoDTO(DTO):
    exigencia: str = field(default_factory=str)
    deporte: str = field(default_factory=str)


@dataclass(frozen=True)
class PlanEntrenamientoDTO(DTO):
    created_at: str = field(default_factory=str)
    updated_at: str = field(default_factory=str)
    id: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    categoria: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    objetivo: ObjetivoEntrenamientoDTO = field(default_factory=ObjetivoEntrenamientoDTO)

    entrenamientos: list[EntrenamientoDTO] = field(default_factory=list)


@dataclass(frozen=True)
class UsuarioPlanDTO(DTO):
    created_at: str = field(default_factory=str)
    updated_at: str = field(default_factory=str)
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
    deportes: list[str] = field(default_factory=list)
    planes_entrenamiento: list[PlanEntrenamientoDTO] = field(default_factory=list)