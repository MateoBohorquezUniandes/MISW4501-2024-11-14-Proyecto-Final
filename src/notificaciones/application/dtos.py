from dataclasses import dataclass, field
import datetime

from seedwork.application.dtos import DTO


@dataclass(frozen=True)
class SendToTopicDTO(DTO):
    titulo: str = field(default_factory=str)
    cuerpo: str = field(default_factory=str)
    topico: str = field(default_factory=str)


@dataclass(frozen=True)
class SubscribeToTopicDTO(DTO):
    tokens: list[str] = field(default_factory=list)
    topico: str = field(default_factory=str)
