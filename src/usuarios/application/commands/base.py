from seedwork.application.commands import CommandHandler
from usuarios.domain.factories import ContrasenaFactory, LoginFactory, UsuarioFactory
from usuarios.infrastructure.factories import RepositoryFactory
from usuarios.infrastructure.services import UsuarioAuthorizationService


class UsuarioBaseHandler(CommandHandler):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._usuarios_factory: UsuarioFactory = UsuarioFactory()
        self._contrasena_factory: ContrasenaFactory = ContrasenaFactory()
        self._login_factory: LoginFactory = LoginFactory()
        self._autenticacion_service: UsuarioAuthorizationService = (
            UsuarioAuthorizationService()
        )

    @property
    def repository_factory(self):
        return self._repository_factory

    @property
    def usuarios_factory(self):
        return self._usuarios_factory

    @property
    def contrasena_factory(self):
        return self._contrasena_factory

    @property
    def login_factory(self):
        return self._login_factory

    @property
    def autenticacion_service(self):
        return self._autenticacion_service
