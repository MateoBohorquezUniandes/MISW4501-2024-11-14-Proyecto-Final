from dataclasses import dataclass, field

from seedwork.infrastructure.schema.v1.events import IntegrationEvent
from seedwork.infrastructure.schema.v1.messages import MessagePayload


@dataclass(frozen=True)
class DemografiaPayload(MessagePayload):
    pais_nacimiento: str = field(default_factory=str)
    ciudad_nacimiento: str = field(default_factory=str)
    pais_residencia: str = field(default_factory=str)
    ciudad_residencia: str = field(default_factory=str)
    tiempo_residencia: int = field(default_factory=int)

    genero: str = field(default_factory=str)
    edad: int = field(default_factory=int)
    peso: float = field(default_factory=float)
    altura: float = field(default_factory=float)


@dataclass(frozen=True)
class FisiologiaPayload(MessagePayload):
    genero: str = field(default_factory=str)
    edad: int = field(default_factory=int)
    peso: float = field(default_factory=float)
    altura: float = field(default_factory=float)


@dataclass(frozen=True)
class UsuarioCreatedPayload(MessagePayload):
    created_at: str = field(default_factory=str)
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
    rol: str = field(default_factory=str)

    demografia: DemografiaPayload = field(default_factory=DemografiaPayload)
    fisiologia: FisiologiaPayload = field(default_factory=DemografiaPayload)
    deportes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class UsuarioCreatedIntegrationEvent(IntegrationEvent):
    payload: UsuarioCreatedPayload = field(default_factory=UsuarioCreatedPayload)
