import uuid
import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError
from usuarios.application.commands.base import UsuarioBaseHandler
from usuarios.application.dtos import UsuarioDTO
from usuarios.application.exceptions import (
    UnprocessableEntityError,
    BadRequestError,
)
from usuarios.application.mappers import ContrasenaMapper, UsuarioDTOEntityMapper
from usuarios.domain.entities import Usuario
from usuarios.domain.exceptions import (
    InvalidRolUsuarioError
)
from usuarios.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory


@dataclass
class CreateUsuario(Command):
    usuario_dto: UsuarioDTO = field(default_factory=UsuarioDTO)


class CreateUsuarioHandler(UsuarioBaseHandler):

    def handle(self, command: CreateUsuario):
        uowf = None
        try:
            usuario: Usuario = self.usuarios_factory.create(
                command.usuario_dto, UsuarioDTOEntityMapper()
            )
            usuario.contrasena = self.contrasena_factory.create(
                command.usuario_dto.contrasena, mapper=ContrasenaMapper()
            )
            usuario.create(command.correlation_id)

            repository = self.repository_factory.create(usuario)
            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()

            UnitOfWorkPort.register_batch(uowf, repository.append, usuario)
            UnitOfWorkPort.commit(uowf)

        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="register.user.integrity")
        except InvalidRolUsuarioError as iure:
            traceback.print_exc()
            raise BadRequestError(str(iure), "register.user.integrity.rol")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="register.error.internal")

@execute_command.register(CreateUsuario)
def command_crear_usuario(command: CreateUsuario):
    CreateUsuarioHandler().handle(command)
