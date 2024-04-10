import traceback
from dataclasses import dataclass, field

from planes.application.mappers import UsuarioPlanDTOEntityMapper
from planes.application.queries.base import PlanQueryBaseHandler
from planes.domain.entities import UsuarioPlan
from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError


@dataclass(frozen=True)
class GetUsuarioPlanes(Query): ...


class GetUsuarioPlanesQueryHandler(PlanQueryBaseHandler):

    def handle(self, query: GetUsuarioPlanes) -> QueryResult:
        try:
            repository = self.repository_factory.create(UsuarioPlan)
            usuarios_plan: list[UsuarioPlan] = repository.get_all()

            mapper = UsuarioPlanDTOEntityMapper()
            usuarios_plan_dto = [
                self.planes_factory.create(e, mapper) for e in usuarios_plan
            ]
            return QueryResult(result=usuarios_plan_dto)

        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="usuario_plan.get.error.internal")


@execute_query.register(GetUsuarioPlanes)
def execute_query_usuario_plan(query: GetUsuarioPlanes):
    return GetUsuarioPlanesQueryHandler().handle(query)
