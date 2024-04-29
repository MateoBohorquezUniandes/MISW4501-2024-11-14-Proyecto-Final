import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import NoResultFound

from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError
from sesiones.application.exceptions import SesionNotFoundError
from sesiones.application.mappers import SesionDeportivaDTOEntityMapper
from sesiones.application.queries.base import SesionQueryBaseHandler
from sesiones.domain.entities import SesionDeportiva


@dataclass
class ObtenerSesion(Query):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
    id: str = field(default_factory=str)


class ObtenerSesionQueryHandler(SesionQueryBaseHandler):

    def handle(self, query: ObtenerSesion) -> QueryResult:
        try:
            repository = self.repository_factory.create(SesionDeportiva)
            sesion: SesionDeportiva = repository.get(
                query.tipo_identificacion, query.identificacion, query.id
            )

            indicadores_external = self.indicadores_service.request(
                "get", f"/indicadores/queries/?idSesion={query.id}"
            )

            sesion.indicadores = indicadores_external.json()
            sesion_dto = self.sesiones_factory.create(
                sesion, SesionDeportivaDTOEntityMapper()
            )

            return QueryResult(result=sesion_dto)

        except NoResultFound:
            traceback.print_exc()
            raise SesionNotFoundError()
        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="sesion.get.error.internal")


@execute_query.register(ObtenerSesion)
def execute_query_sesion(query: ObtenerSesion):
    return ObtenerSesionQueryHandler().handle(query)
