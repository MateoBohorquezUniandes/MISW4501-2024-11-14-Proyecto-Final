from dataclasses import dataclass, field

from seedwork.application.dtos import DTO


@dataclass(frozen=True)
class ObjetivoDTO(DTO):
    exigencia: str = field(default_factory=str)
    deporte: str = field(default_factory=str)


@dataclass(frozen=True)
class SesionDeportivaDTO(DTO):
    id: str = field(default_factory=str)
    created_at: str = field(default_factory=str)
    updated_at: str = field(default_factory=str)

    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
    completed_at: str = field(default_factory=str)

    objetivo: ObjetivoDTO = field(default_factory=ObjetivoDTO)
    indicadores: list[dict] = field(default_factory=list)
