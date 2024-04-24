import traceback
from dataclasses import dataclass, field

from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError

from eventos.application.queries.base import EventoQueryBaseHandler
from eventos.domain.entities import Evento
from eventos.application.mappers import EventoDTOEntityMapper


class GetEventos(Query):

    def __init__(self, lugar=None, fecha=None, nivel=None):
        self.lugar = lugar
        self.fecha = fecha
        self.nivel = nivel


class GetEventosQueryHandler(EventoQueryBaseHandler):

    def handle(self, query: GetEventos) -> QueryResult:
        try:
            repository = self.repository_factory.create(Evento)
            eventos: list[Evento] = repository.get_all(
                query.lugar, query.fecha, query.nivel
            )

            mapper = EventoDTOEntityMapper()
            eventos_dto = [self.eventos_factory.create(e, mapper) for e in eventos]
            return QueryResult(result=eventos_dto)

        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="eventos.get.error.internal")


@execute_query.register(GetEventos)
def execute_query_eventos(query: GetEventos):
    return GetEventosQueryHandler().handle(query)
