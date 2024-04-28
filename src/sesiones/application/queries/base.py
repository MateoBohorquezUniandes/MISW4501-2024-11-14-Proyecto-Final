from sesiones.domain.factories import SesionFactory
from sesiones.infrastructure.factories import RepositoryFactory
from seedwork.application.queries import QueryHandler
from sesiones.infrastructure.services import IndicadoresAPIService


class SesionQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._sesiones_factory: SesionFactory = SesionFactory()
        self._indicadores_service: IndicadoresAPIService = IndicadoresAPIService()

    @property
    def repository_factory(self):
        return self._repository_factory

    @property
    def sesiones_factory(self):
        return self._sesiones_factory

    @property
    def indicadores_service(self):
        return self._indicadores_service
