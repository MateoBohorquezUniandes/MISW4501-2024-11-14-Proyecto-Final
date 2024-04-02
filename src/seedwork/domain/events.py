import uuid
from dataclasses import dataclass, field
from datetime import datetime

from .exceptions import MutableEntityIdException
from .rules import ImmutableEntityIdRule


@dataclass
class DomainEvent:
    id: uuid.UUID = field(hash=True)
    _id: uuid.UUID = field(init=False, repr=False, hash=True)

    correlation_id: uuid.UUID = field(default_factory=uuid.uuid4)
    tiemstamp: datetime = field(default=datetime.now())

    @classmethod
    def siguiente_id(self) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: uuid.UUID) -> None:
        if not ImmutableEntityIdRule(self).is_valid():
            raise MutableEntityIdException()
        self._id = self.siguiente_id()
