from dataclasses import dataclass
from .messages import IntegrationMessage


@dataclass(frozen=True)
class IntegrationCommand(IntegrationMessage): ...
