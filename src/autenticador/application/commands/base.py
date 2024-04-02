from seedwork.application.commands import CommandHandler
from autenticador.domain.factories import TokenRequestFactory


class CommandBaseHandler(CommandHandler):
    def __init__(self):
        self._token_factory: TokenRequestFactory = TokenRequestFactory()

    @property
    def token_factory(self):
        return self._token_factory
