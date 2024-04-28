import traceback
from dataclasses import dataclass, field

from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError
from sesiones.application.exceptions import SesionNotFoundError
from sesiones.application.mappers import SesionDeportivaDTOEntityMapper
from sesiones.application.queries.base import SesionQueryBaseHandler
from sesiones.domain.entities import SesionDeportiva


@dataclass
class ObtenerSesiones(Query):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)


class ObtenerSesionesQueryHandler(SesionQueryBaseHandler):

    def handle(self, query: ObtenerSesiones) -> QueryResult:
        try:
            repository = self.repository_factory.create(SesionDeportiva)
            sesiones: list[SesionDeportiva] = repository.get_all(
                query.tipo_identificacion, query.identificacion
            )

            mapper = SesionDeportivaDTOEntityMapper()
            sesiones_dto = [self.sesiones_factory.create(e, mapper) for e in sesiones]
            return QueryResult(result=sesiones_dto)

        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="sesiones.get.error.internal")


@execute_query.register(ObtenerSesiones)
def execute_query_sesiones(query: ObtenerSesiones):
    return ObtenerSesionesQueryHandler().handle(query)
