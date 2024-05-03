import traceback
from dataclasses import dataclass

from planes.application.mappers import PlanEntrenamientoDTOEntityMapper
from planes.application.queries.base import PlanQueryBaseHandler
from planes.domain.entities import PlanEntrenamiento
from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError


@dataclass(frozen=True)
class GetPlanesEnternamiento(Query): ...


class GetPlanesEnternamientoQueryHandler(PlanQueryBaseHandler):

    def handle(self, query: GetPlanesEnternamiento) -> QueryResult:
        try:
            repository = self.repository_factory.create(PlanEntrenamiento)
            planes: list[PlanEntrenamiento] = repository.get_all()

            mapper = PlanEntrenamientoDTOEntityMapper()
            return QueryResult(
                result=[self.planes_factory.create(e, mapper) for e in planes]
            )

        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="entrenamientos.get.error.internal")


@execute_query.register(GetPlanesEnternamiento)
def execute_query_planes_entrenamiento(query: GetPlanesEnternamiento):
    return GetPlanesEnternamientoQueryHandler().handle(query)
