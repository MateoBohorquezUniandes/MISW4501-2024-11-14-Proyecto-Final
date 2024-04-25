import uuid
from dataclasses import dataclass, field
from datetime import datetime

import sesiones.domain.value_objects as vo
from seedwork.domain.entities import RootAggregation
from sesiones.domain.events import SesionEnded


@dataclass
class SesionDeportiva(RootAggregation):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)

    objetivo: vo.Objetivo = field(default_factory=vo.Objetivo)
    completed_at: datetime = field(default=None)

    def create(self, correlation_id: uuid.UUID):
        pass

    def end(self, correlation_id: uuid.UUID, parametros: dict):
        self.append_event(
            SesionEnded(
                self.id,
                correlation_id=correlation_id,
                tipo_identificacion=self.tipo_identificacion,
                identificacion=self.identificacion,
                parametros=parametros,
            )
        )
