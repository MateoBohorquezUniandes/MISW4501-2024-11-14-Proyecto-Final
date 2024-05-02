import traceback
from dataclasses import dataclass, field

from planes.application.mappers import RutinaAlimentacionDTOEntityMapper
from planes.application.queries.base import PlanQueryBaseHandler
from planes.domain.entities import RutinaAlimentacion
from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError


@dataclass(frozen=True)
class GetRutinasAlimentacion(Query):
    tipo_alimentacion: str = field(default=None)
    deporte: str = field(default=None)


class GetRutinasAlimentacionQueryHandler(PlanQueryBaseHandler):

    def handle(self, query: GetRutinasAlimentacion) -> QueryResult:
        try:
            repository = self.repository_factory.create(RutinaAlimentacion)
            rutinas: list[RutinaAlimentacion] = repository.get_all(
                query.tipo_alimentacion, query.deporte
            )

            mapper = RutinaAlimentacionDTOEntityMapper()
            planes_dto = [self.planes_factory.create(e, mapper) for e in rutinas]
            print(planes_dto)
            return QueryResult(result=planes_dto)

        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="rutinas.get.error.internal")


@execute_query.register(GetRutinasAlimentacion)
def execute_query_planes_rutina(query: GetRutinasAlimentacion):
    return GetRutinasAlimentacionQueryHandler().handle(query)
