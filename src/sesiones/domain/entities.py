from dataclasses import dataclass, field
from datetime import datetime
import uuid

from seedwork.domain.entities import RootAggregation
import sesiones.domain.value_objects as vo


@dataclass
class SesionDeportiva(RootAggregation):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)

    objetivo: vo.Objetivo = field(default_factory=vo.Objetivo)
    completed_at: datetime = field(default=None)

    def create(self, correlation_id: uuid.UUID):
        pass

    def end(self, correlation_id: uuid.UUID, parameters: dict):
        pass
