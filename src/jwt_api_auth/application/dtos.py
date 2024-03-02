import datetime
from dataclasses import dataclass, field

from seedwork.application.dtos import DTO

@dataclass(frozen=True)
class TokenDTO(DTO):
    user: str
    password: str