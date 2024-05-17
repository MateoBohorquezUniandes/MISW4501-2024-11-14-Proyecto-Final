from seedwork.application.commands import CommandHandler
from usuarios.domain.factories import UsuarioFactory
from usuarios.infrastructure.factories import RepositoryFactory


class UsuarioBaseHandler(CommandHandler):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._usuarios_factory: UsuarioFactory = UsuarioFactory()

    @property
    def repository_factory(self):
        return self._repository_factory

    @property
    def usuarios_factory(self):
        return self._usuarios_factory
