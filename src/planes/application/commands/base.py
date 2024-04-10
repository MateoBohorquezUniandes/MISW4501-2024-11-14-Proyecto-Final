from planes.domain.factories import PlanFactory
from planes.infrastructure.factories import RepositoryFactory
from seedwork.application.commands import CommandHandler


class PlanCommandBaseHandler(CommandHandler):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._planes_factory: PlanFactory = PlanFactory()

    @property
    def repository_factory(self):
        return self._repository_factory

    @property
    def planes_factory(self):
        return self._planes_factory
