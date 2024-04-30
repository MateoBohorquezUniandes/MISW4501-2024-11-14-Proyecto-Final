import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import NoResultFound

from perfiles.application.exceptions import PerfilNotFoundError
from perfiles.application.mappers import (
    AlimentoDTOEntityMapper,
    PerfilAlimenticioDTOEntityMapper,
)
from perfiles.application.queries.base import PerfilQueryBaseHandler
from perfiles.domain.entities import Alimento, PerfilAlimenticio
from perfiles.domain.value_objects import AlimentoAsociado
from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError


@dataclass(frozen=True)
class ObtenerPerfilAlimenticio(Query):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)


class ObtenerPerfilAlimenticioQueryHandler(PerfilQueryBaseHandler):

    def handle(self, query: ObtenerPerfilAlimenticio) -> QueryResult:
        try:
            repository = self.repository_factory.create(AlimentoAsociado)
            alimentos = repository.get_all(
                query.tipo_identificacion, query.identificacion
            )
            mapper = AlimentoDTOEntityMapper()
            alimentos = [self.perfiles_factory.create(a, mapper) for a in alimentos]
            perfil = PerfilAlimenticio(
                tipo_identificacion=query.tipo_identificacion,
                identificacion=query.identificacion,
                alimentos=alimentos,
            )

            return QueryResult(
                result=self.perfiles_factory.create(
                    perfil, PerfilAlimenticioDTOEntityMapper()
                )
            )

        except NoResultFound:
            traceback.print_exc()
            raise PerfilNotFoundError()
        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="alimentos.get.error.internal")


@execute_query.register(ObtenerPerfilAlimenticio)
def execute_query_perfil_alimenticio(query: ObtenerPerfilAlimenticio):
    return ObtenerPerfilAlimenticioQueryHandler().handle(query)
