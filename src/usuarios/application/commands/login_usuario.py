import traceback
import uuid
from dataclasses import dataclass, field

from sqlalchemy.exc import NoResultFound

from seedwork.application.commands import Command, CommandResult, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.presentation.exceptions import APIError
from usuarios.application.commands.base import UsuarioBaseHandler
from usuarios.application.dtos import LoginRequestDTO
from usuarios.application.exceptions import (
    InvalidCredentialsError,
    UnprocessableEntityError,
    UsuarioNotFoundError,
)
from usuarios.application.mappers import (
    AuthResponseDTODictMapper,
    ContrasenaMapper,
    LoginDTOEntityMapper,
)
from usuarios.domain.entities import Deportista, Organizador, Socio
from usuarios.domain.exceptions import InvalidPasswordMatchError
from usuarios.domain.value_objects import ROL, LoginRequest

usuario_map = {
    ROL.DEPORTISTA.value: Deportista,
    ROL.ORGANIZADOR.value: Organizador,
    ROL.SOCIO.value: Socio,
}


@dataclass
class LoginUsuario(Command):
    login_request: LoginRequestDTO
    correlation_id: uuid.UUID = field(default_factory=uuid.uuid4)


class LoginUsuarioHandler(UsuarioBaseHandler):

    def handle(self, command: LoginUsuario):
        try:
            login: LoginRequest = self.login_factory.create(
                command.login_request, LoginDTOEntityMapper()
            )

            # Get user from DB
            repository = self.repository_factory.create(usuario_map[login.rol]())
            usuario = repository.get(
                login.identificacion.tipo, login.identificacion.valor, login.rol
            )

            # Validate credentiales
            contrasena = self.contrasena_factory.create(
                command.login_request.contrasena,
                usuario.contrasena.salt,
                ContrasenaMapper(),
            )
            contrasena.match(usuario.contrasena.contrasena, raise_exception=True)

            auth_mapper = AuthResponseDTODictMapper()
            auth_external = self.autenticacion_service.request(
                login.identificacion.__dict__
            )
            login_response = auth_mapper.external_to_dto(auth_external, usuario.rol)

            return CommandResult(result=login_response)

        except InvalidPasswordMatchError as ipme:
            traceback.print_exc()
            raise InvalidCredentialsError(str(ipme), ipme.code)
        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except NoResultFound:
            traceback.print_exc()
            raise UsuarioNotFoundError()
        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="login.error.internal")


@execute_command.register(LoginUsuario)
def command_login_usuario(command: LoginUsuario) -> CommandResult:
    return LoginUsuarioHandler().handle(command)
