from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import singledispatch
from typing import Optional


class Command: ...


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
