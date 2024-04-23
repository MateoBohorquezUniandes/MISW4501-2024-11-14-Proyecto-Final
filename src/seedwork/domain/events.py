import uuid
from dataclasses import dataclass, field
from datetime import datetime

from .exceptions import MutableEntityIdException
from .rules import ImmutableEntityIdRule


@dataclass
class DomainEvent:
    _id: uuid.UUID = field(default_factory=uuid.uuid4, repr=False, hash=True)
    correlation_id: uuid.UUID = field(default_factory=uuid.uuid4)
    tiemstamp: datetime = field(default=datetime.now())

    def __post_init__(self):
        if not self.id:
            self._id = uuid.uuid4()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: uuid.UUID) -> None:
        if not ImmutableEntityIdRule(self).is_valid():
            raise MutableEntityIdException()
        self._id = id
