import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import NoResultFound

from perfiles.application.exceptions import PerfilNotFoundError
from perfiles.application.mappers import PerfilDeportivoDTOEntityMapper
from perfiles.application.queries.base import PerfilQueryBaseHandler
from perfiles.domain.entities import PerfilDeportivo
from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError


@dataclass(frozen=True)
class ObtenerPerfilDeportivo(Query):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)


class ObtenerPerfilDeportivoQueryHandler(PerfilQueryBaseHandler):

    def handle(self, query: ObtenerPerfilDeportivo) -> QueryResult:
        try:
            repository = self.repository_factory.create(PerfilDeportivo)
            perfil = repository.get(query.tipo_identificacion, query.identificacion)

            return QueryResult(
                result=self.perfiles_factory.create(
                    perfil, PerfilDeportivoDTOEntityMapper()
                )
            )

        except NoResultFound:
            traceback.print_exc()
            raise PerfilNotFoundError()
        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="perfiles.get.error.internal")


@execute_query.register(ObtenerPerfilDeportivo)
def execute_query_perfil_demografico(query: ObtenerPerfilDeportivo):
    return ObtenerPerfilDeportivoQueryHandler().handle(query)
