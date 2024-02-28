import uuid
from dataclasses import dataclass, field
from datetime import datetime

from .events import DomainEvent
from .exceptions import MutableEntityIdException
from .mixins import RuleValidationMixin
from .rules import ImmutableEntityIdRule

@dataclass
class Entity:
    id: uuid.UUID = field(hash=True)
    _id: uuid.UUID = field(init=False, repr=False, hash=True)
    created_at: datetime = field(default=datetime.now())
    updated_at: datetime = field(default=datetime.now())

    @classmethod
    def next_id(self) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: uuid.UUID) -> None:
        if not ImmutableEntityIdRule(self).is_valid():
            raise MutableEntityIdException()
        self._id = self.next_id()


@dataclass
class RootAggregation(Entity, RuleValidationMixin):
    events: list[DomainEvent] = field(default_factory=list)

    def append_event(self, evento: DomainEvent):
        self.events.append(evento)

    def clear_events(self):
        self.events = list()
