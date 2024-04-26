import traceback
from dataclasses import dataclass, field

from indicadores.application.mappers import FormulaDTOEntityMapper
from indicadores.application.queries.base import IndicadorQueryBaseHandler
from indicadores.domain.entities import Formula
from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError


@dataclass(frozen=True)
class GetFormulas(Query):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)

class GetFormulasQueryHandler(IndicadorQueryBaseHandler):

    def handle(self, query: GetFormulas) -> QueryResult:
        try:
            repository = self.repository_factory.create(Formula)
            formulas: list[Formula] = repository.get(query.tipo_identificacion, query.identificacion)

            mapper = FormulaDTOEntityMapper()
            formulas_dto = [self.indices_factory.create(e, mapper) for e in formulas]
            return QueryResult(result=formulas_dto)

        except Exception as e:
            traceback.print_exc()
            raise APIError(
                message=str(e), code="indicadores.get.error.internal"
            )

@execute_query.register(GetFormulas)
def execute_query_formulas(query: GetFormulas):
    return GetFormulasQueryHandler().handle(query)
