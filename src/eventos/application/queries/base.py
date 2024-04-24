from eventos.domain.factories import EventoFactoy
from eventos.infrastructure.factories import RepositoryFactory
from seedwork.application.queries import QueryHandler


class EventoQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._eventos_factory: EventoFactoy = EventoFactoy()

    @property
    def repository_factory(self):
        return self._repository_factory

    @property
    def eventos_factory(self):
        return self._eventos_factory
