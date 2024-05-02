import traceback
from dataclasses import dataclass

from perfiles.application.mappers import AlimentoDTOEntityMapper
from perfiles.application.queries.base import PerfilQueryBaseHandler
from perfiles.domain.entities import Alimento
from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError


@dataclass(frozen=True)
class ObtenerAlimentos(Query): ...


class ObtenerAlimentosQueryHandler(PerfilQueryBaseHandler):

    def handle(self, query: ObtenerAlimentos) -> QueryResult:
        try:
            repository = self.repository_factory.create(Alimento)
            alimentos: list[Alimento] = repository.get_all()

            mapper = AlimentoDTOEntityMapper()
            alimentos_dto = [self._perfiles_factory.create(e, mapper) for e in alimentos]
            print(alimentos_dto)
            return QueryResult(result=alimentos_dto)

        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="alimentos.get.error.internal")


@execute_query.register(ObtenerAlimentos)
def execute_query_perfiles_deportivos(query: ObtenerAlimentos):
    return ObtenerAlimentosQueryHandler().handle(query)
