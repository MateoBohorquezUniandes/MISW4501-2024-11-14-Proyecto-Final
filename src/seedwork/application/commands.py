from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import singledispatch
from typing import Optional
import uuid


@dataclass
class Command:
    correlation_id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        if not self.correlation_id:
            self.correlation_id = uuid.uuid4()


@dataclass
class CommandResult:
    result: any


class CommandHandler(ABC):
    @abstractmethod
    def handle(self, command: Command):
        raise NotImplementedError()


@singledispatch
def execute_command(command) -> Optional[CommandResult]:
    raise NotImplementedError(
        f"Missing command execution implementation for {type(command).__name__}"
    )
