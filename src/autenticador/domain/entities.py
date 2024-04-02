import datetime
from dataclasses import dataclass, field

from autenticador.domain.events import TokenCreated
from autenticador.domain.value_objects import Identidad
from seedwork.domain.entities import Entity, RootAggregation


@dataclass
class Token(Entity):
    valor: str = field(default_factory=str)
    expiration_delta: datetime = field(
        default_factory=lambda: datetime.timedelta(hours=7)
    )


@dataclass
class Autenticacion(RootAggregation):
    identity: Identidad = field(default_factory=Identidad)
    token: Token = field(default_factory=Token)

