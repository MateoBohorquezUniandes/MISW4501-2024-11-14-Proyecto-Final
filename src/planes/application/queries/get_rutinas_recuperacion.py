import traceback
from dataclasses import dataclass, field

from planes.application.mappers import RutinaRecuperacionDTOEntityMapper
from planes.application.queries.base import PlanQueryBaseHandler
from planes.domain.entities import RutinaRecuperacion
from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError


@dataclass(frozen=True)
class GetRutinasRecuperacion(Query):
    deporte: str = field(default=None)


class GetRutinasRecuperacionQueryHandler(PlanQueryBaseHandler):

    def handle(self, query: GetRutinasRecuperacion) -> QueryResult:
        try:
            repository = self.repository_factory.create(RutinaRecuperacion)
            rutinas: list[RutinaRecuperacion] = repository.get_all(query.deporte)

            mapper = RutinaRecuperacionDTOEntityMapper()
            planes_dto = [self.planes_factory.create(e, mapper) for e in rutinas]
            print(planes_dto)
            return QueryResult(result=planes_dto)

        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="rutinas.get.error.internal")


@execute_query.register(GetRutinasRecuperacion)
def execute_query_rutinas_recuperacion(query: GetRutinasRecuperacion):
    return GetRutinasRecuperacionQueryHandler().handle(query)
