import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import NoResultFound

from planes.application.exceptions import UserNotFoundError
from planes.application.mappers import UsuarioPlanDTOEntityMapper
from planes.application.queries.base import PlanQueryBaseHandler
from planes.domain.entities import UsuarioPlan
from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError


@dataclass(frozen=True)
class GetPlanesAsociadosUsuario(Query):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)


class GetPlanesAsociadosUsuarioQueryHandler(PlanQueryBaseHandler):

    def handle(self, query: GetPlanesAsociadosUsuario) -> QueryResult:
        try:
            repository = self.repository_factory.create(UsuarioPlan)
            usuario_planes_asociados = repository.get(
                query.tipo_identificacion, query.identificacion
            )

            mapper = UsuarioPlanDTOEntityMapper()

            usuario_planes_asociados_dto = self.planes_factory.create(
                usuario_planes_asociados, mapper
            )

            return QueryResult(result=usuario_planes_asociados_dto)

        except NoResultFound:
            traceback.print_exc()
            raise UserNotFoundError()

        except Exception as e:
            traceback.print_exc()
            raise APIError(
                message=str(e), code="usuario_plan_asociado.get.error.internal"
            )


@execute_query.register(GetPlanesAsociadosUsuario)
def execute_query_usuario_plan(query: GetPlanesAsociadosUsuario):
    return GetPlanesAsociadosUsuarioQueryHandler().handle(query)
