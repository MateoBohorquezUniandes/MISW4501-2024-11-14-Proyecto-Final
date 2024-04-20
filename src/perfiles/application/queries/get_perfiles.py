import traceback
from dataclasses import dataclass

from perfiles.application.mappers import PerfilDeportivoDTOEntityMapper
from perfiles.application.queries.base import PerfilQueryBaseHandler
from perfiles.domain.entities import PerfilDeportivo
from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError


@dataclass(frozen=True)
class GetPerfilesDeportivos(Query): ...


class GetPerfilesDeportivosQueryHandler(PerfilQueryBaseHandler):

    def handle(self, query: GetPerfilesDeportivos) -> QueryResult:
        try:
            repository = self.repository_factory.create(PerfilDeportivo)
            perfiles: list[PerfilDeportivo] = repository.get_all()

            mapper = PerfilDeportivoDTOEntityMapper()
            perfiles_dto = [self._perfiles_factory.create(e, mapper) for e in perfiles]
            return QueryResult(result=perfiles_dto)

        except Exception as e:
            traceback.print_exc()
            raise APIError(
                message=str(e), code="perfiles_derportivos.get.error.internal"
            )


@execute_query.register(GetPerfilesDeportivos)
def execute_query_perfiles_deportivos(query: GetPerfilesDeportivos):
    return GetPerfilesDeportivosQueryHandler().handle(query)
