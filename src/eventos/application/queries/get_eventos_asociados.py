import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import NoResultFound

from eventos.application.exceptions import EventoNotFoundError
from eventos.application.mappers import EventoDTOEntityMapper
from eventos.application.queries.base import EventoQueryBaseHandler
from eventos.domain.value_objects import EventoAsociado
from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError


@dataclass(frozen=True)
class ObtenerEventosAsociados(Query):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
    programado: bool = field(default=False)


class ObtenerEventosAsociadosQueryHandler(EventoQueryBaseHandler):

    def handle(self, query: ObtenerEventosAsociados) -> QueryResult:
        try:
            repository = self.repository_factory.create(EventoAsociado)
            eventos = repository.get_all(
                query.tipo_identificacion, query.identificacion, query.programado
            )

            mapper = EventoDTOEntityMapper()
            return QueryResult(
                result=[self.eventos_factory.create(a, mapper) for a in eventos]
            )

        except NoResultFound:
            traceback.print_exc()
            raise EventoNotFoundError()
        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="eventos.get.error.internal")


@execute_query.register(ObtenerEventosAsociados)
def execute_query_perfil_alimenticio(query: ObtenerEventosAsociados):
    return ObtenerEventosAsociadosQueryHandler().handle(query)
