from seedwork.application.commands import CommandHandler
from jwt_api_auth.infrastructure.repositories import RepositorioTokenSQLite

class TokenBaseHandler(CommandHandler):
    def __init__(self):
        self._fabrica_repositorio: RepositorioTokenSQLite = RepositorioTokenSQLite()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio