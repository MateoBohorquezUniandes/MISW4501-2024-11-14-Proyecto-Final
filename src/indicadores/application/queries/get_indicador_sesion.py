import traceback
from dataclasses import dataclass, field
from sqlalchemy.exc import NoResultFound

from indicadores.application.exceptions import IndicadorNotFoundError
from indicadores.application.mappers import IndicadorDTOEntityMapper
from indicadores.application.queries.base import IndicadorQueryBaseHandler
from indicadores.domain.entities import Indicador, Formula
from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError


@dataclass(frozen=True)
class GetIndicadorSesion(Query):
    session_id: str = field(default_factory=str)

class GetIndicadorSesionQueryHandler(IndicadorQueryBaseHandler):

    def handle(self, query: GetIndicadorSesion) -> QueryResult:
        try:
            repository = self.repository_factory.create(Indicador)
            repository_f = self.repository_factory.create(Formula)
            indicador: Indicador = repository.get_for_session_id(query.session_id)
            formula: Formula = repository_f.get_by_id(indicador.idFormula)
            indicador.nombreFormula = formula.nombre
            mapper = IndicadorDTOEntityMapper()
            indicador_dto = self.indices_factory.create(indicador, mapper)
            return QueryResult(result=indicador_dto)

        except NoResultFound:
            traceback.print_exc()
            raise IndicadorNotFoundError()
        except Exception as e:
            traceback.print_exc()
            raise APIError(
                message=str(e), code="indicadores.get.error.internal"
            )

@execute_query.register(GetIndicadorSesion)
def execute_query_formulas(query: GetIndicadorSesion):
    return GetIndicadorSesionQueryHandler().handle(query)