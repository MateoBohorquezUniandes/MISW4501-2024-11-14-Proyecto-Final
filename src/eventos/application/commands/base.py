from eventos.domain.factories import EventoFactory
from eventos.infrastructure.factories import RepositoryFactory

from seedwork.application.commands import CommandHandler


class EventoCommandBaseHandler(CommandHandler):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._eventos_factory: EventoFactory = EventoFactory()

    @property
    def repository_factory(self):
        return self._repository_factory

    @property
    def perfiles_factory(self):
        return self._eventos_factory
