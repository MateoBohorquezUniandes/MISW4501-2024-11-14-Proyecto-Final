import datetime
from dataclasses import dataclass, field

from seedwork.domain.events import DomainEvent


@dataclass
class UsuarioCreated(DomainEvent):
    tipo_identificacion: str = None
    identificacion: str = None
    rol: str = None
    created_at: datetime = None

    demografia: dict = None
    deportes: dict = None
