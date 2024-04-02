from dataclasses import dataclass, field

from seedwork.application.dtos import DTO


@dataclass(frozen=True)
class IdentificacionDTO(DTO):
    tipo: str
    valor: str


@dataclass(frozen=True)
class DemografiaDTO(DTO):
    pais_nacimiento: str
    ciudad_nacimiento: str

    pais_residencia: str
    ciudad_residencia: str
    tiempo_residencia: int

    genero: str
    edad: int
    peso: float
    altura: float


@dataclass(frozen=True)
class UsuarioDTO(DTO):
    created_at: str = field(default_factory=str)
    updated_at: str = field(default_factory=str)

    nombre: str = field(default_factory=str)
    apellido: str = field(default_factory=str)

    rol: str = field(default_factory=str)
    contrasena: str = field(default_factory=str)
    identificacion: IdentificacionDTO = field(default_factory=IdentificacionDTO)

    demografia: DemografiaDTO = field(default_factory=DemografiaDTO)
    deportes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class LoginRequestDTO(DTO):
    identificacion: IdentificacionDTO = field(default_factory=IdentificacionDTO)
    contrasena: str = field(default_factory=str)


@dataclass(frozen=True)
class LoginResponseDTO(DTO):
    rol: str = field(default_factory=str)
    token: str = field(default_factory=str)
