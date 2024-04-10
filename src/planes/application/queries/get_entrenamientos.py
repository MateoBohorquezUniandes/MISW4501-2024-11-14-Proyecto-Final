import traceback
from dataclasses import dataclass, field

from planes.application.mappers import EntrenamientoDTOEntityMapper
from planes.application.queries.base import PlanQueryBaseHandler
from planes.domain.entities import Entrenamiento
from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError


@dataclass(frozen=True)
class GetEnternamientos(Query): ...


class GetEnternamientosQueryHandler(PlanQueryBaseHandler):

    def handle(self, query: GetEnternamientos) -> QueryResult:
        try:
            repository = self.repository_factory.create(Entrenamiento)
            entrenamientos: list[Entrenamiento] = repository.get_all()

            mapper = EntrenamientoDTOEntityMapper()
            entrenamientos_dto = [
                self.planes_factory.create(e, mapper) for e in entrenamientos
            ]
            return QueryResult(result=entrenamientos_dto)

        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="entrenamientos.get.error.internal")


@execute_query.register(GetEnternamientos)
def execute_query_entrenamientos(query: GetEnternamientos):
    return GetEnternamientosQueryHandler().handle(query)
