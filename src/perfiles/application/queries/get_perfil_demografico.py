import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import NoResultFound

import perfiles.domain.value_objects as vo
from perfiles.application.exceptions import PerfilNotFoundError
from perfiles.application.queries.base import PerfilQueryBaseHandler
from perfiles.domain.entities import PerfilDemografico
from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError


@dataclass(frozen=True)
class ObtenerPerfilDemografico(Query):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)


class ObtenerPerfilDemograficoQueryHandler(PerfilQueryBaseHandler):

    def handle(self, query: ObtenerPerfilDemografico) -> QueryResult:
        try:
            repository = self.repository_factory.create(PerfilDemografico())
            perfil = repository.get(
                query.tipo_identificacion, query.identificacion
            )
            return QueryResult(result=perfil)

        except NoResultFound:
            traceback.print_exc()
            raise PerfilNotFoundError()
        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="perfiles.get.error.internal")


@execute_query.register(ObtenerPerfilDemografico)
def execute_query_perfil_demografico(query: ObtenerPerfilDemografico):
    return ObtenerPerfilDemograficoQueryHandler().handle(query)
