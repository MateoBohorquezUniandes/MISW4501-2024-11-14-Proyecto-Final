import traceback
from dataclasses import dataclass, field

from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError

from eventos.application.queries.base import EventoQueryBaseHandler
from eventos.domain.entities import Evento
from eventos.application.mappers import EventoDTOEntityMapper


@dataclass(frozen=True)
class GetEventos(Query): ...


class GetEventosQueryHandler(EventoQueryBaseHandler):

    def handle(self, query: GetEventos) -> QueryResult:
        try:
            repository = self.repository_factory.create(Evento)
            eventos: list[Evento] = repository.get_all()

            mapper = EventoDTOEntityMapper()
            eventos_dto = [self.eventos_factory.create(e, mapper) for e in eventos]
            return QueryResult(result=eventos_dto)

        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="eventos.get.error.internal")


@execute_query.register(GetEventos)
def execute_query_eventos(query: GetEventos):
    return GetEventosQueryHandler().handle(query)
