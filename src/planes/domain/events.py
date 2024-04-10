import datetime
from dataclasses import dataclass, field

from seedwork.domain.events import DomainEvent


@dataclass
class PlanEntrenamientoCreated(DomainEvent):
    id: str = None
    nombre: str = None
    created_at: datetime = None


@dataclass
class EntrenamientoCreated(DomainEvent):
    id: str = None
    nombre: str = None
    created_at: datetime = None

@dataclass
class UsuarioPlanCreated(DomainEvent):
    tipo_identificacion: str = None
    identificacion: str = None
    created_at: datetime = None
