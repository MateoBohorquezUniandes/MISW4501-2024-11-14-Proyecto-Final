import traceback
import uuid
from dataclasses import dataclass, field

from autenticador.application.commands.base import CommandBaseHandler
from autenticador.application.dtos import TokenRequestDTO
from autenticador.application.exception import UnprocessableTokenRequestError
from autenticador.application.mappers import AutenticacionEntityDTOMapper
from seedwork.application.commands import Command, CommandResult, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.presentation.exceptions import APIError


@dataclass
class CreateToken(Command):
    request: TokenRequestDTO
    correlation_id: uuid.UUID = field(default_factory=uuid.uuid4)


class CreateTokenHandler(CommandBaseHandler):
    def handle(self, command: CreateToken) -> CommandResult:
        try:
            autenticacion = self.token_factory.create(
                command.request, AutenticacionEntityDTOMapper()
            )

            token = self.token_factory.create(
                autenticacion, AutenticacionEntityDTOMapper()
            )

            return CommandResult(result=token)

        except BusinessRuleException as be:
            raise UnprocessableTokenRequestError()
        except Exception:
            raise APIError()


@execute_command.register(CreateToken)
def command_create_token(command: CreateToken):
    return CreateTokenHandler().handle(command)
