from dataclasses import dataclass, field
import uuid

@dataclass(frozen=True)
class IntegrationMessage:
    correlation_id: str = field(default_factory=str)
    specversion: str = field(default_factory=str)
    type: str = field(default_factory=str)
    datacontenttype: str = field(default_factory=str)


@dataclass(frozen=True)
class MessagePayload: ...