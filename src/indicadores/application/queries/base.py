from indicadores.domain.factories import IndicadorFactory
from indicadores.infrastructure.factories import RepositoryFactory
from seedwork.application.queries import QueryHandler


class IndicadorQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._indices_factory: IndicadorFactory = IndicadorFactory()

    @property
    def repository_factory(self):
        return self._repository_factory

    @property
    def indices_factory(self):
        return self._indices_factory