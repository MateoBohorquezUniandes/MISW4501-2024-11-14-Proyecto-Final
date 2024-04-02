import datetime
from dataclasses import dataclass

from seedwork.domain.events import DomainEvent


@dataclass
class TokenCreated(DomainEvent):
    identity: dict = None
    created_at: datetime = None
