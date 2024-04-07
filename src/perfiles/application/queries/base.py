from perfiles.domain.factories import PerfilFactory
from perfiles.infrastructure.factories import RepositoryFactory
from seedwork.application.queries import QueryHandler


class PerfilQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._perfiles_factory: PerfilFactory = PerfilFactory()

    @property
    def repository_factory(self):
        return self._repository_factory

    @property
    def perfiles_factory(self):
        return self._perfiles_factory
