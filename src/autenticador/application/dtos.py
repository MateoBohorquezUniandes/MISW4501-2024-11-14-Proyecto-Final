from dataclasses import dataclass, field

from seedwork.application.dtos import DTO


@dataclass(frozen=True)
class IdentidadDTO(DTO):
    tipo: str = field(default_factory=str)
    valor: str = field(default_factory=str)
    rol: str = field(default_factory=str)


@dataclass(frozen=True)
class TokenRequestDTO(DTO):
    identity: IdentidadDTO = field(default_factory=IdentidadDTO)


@dataclass(frozen=True)
class TokenResponseDTO(DTO):
    token: str = field(default_factory=str)
