from sesiones.domain.factories import SesionFactory
from sesiones.infrastructure.factories import RepositoryFactory
from seedwork.application.commands import CommandHandler


class SesionCommandBaseHandler(CommandHandler):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._sesiones_factory: SesionFactory = SesionFactory()

    @property
    def repository_factory(self):
        return self._repository_factory

    @property
    def sesiones_factory(self):
        return self._sesiones_factory
