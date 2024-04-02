import datetime
import uuid
from dataclasses import dataclass, field

from seedwork.domain.events import DomainEvent


@dataclass
class UsuarioCreated(DomainEvent):
    id_usuario: uuid.UUID = None
    created_at: datetime = None

    demografia: dict = None
    deportes: dict = None
