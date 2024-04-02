import traceback
import uuid
from dataclasses import dataclass, field

from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError
from usuarios.application.commands.base import UsuarioBaseHandler
from usuarios.application.dtos import UsuarioDTO
from usuarios.application.exceptions import UnprocessableEntityError
from usuarios.application.mappers import ContrasenaMapper, UsuarioDTOEntityMapper
from usuarios.domain.entities import Usuario
from usuarios.domain.repositories import UsuarioRepository
from usuarios.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory


@dataclass
class CreateUsuario(Command):
    usuario_dto: UsuarioDTO
    correlation_id: uuid.UUID = field(default_factory=uuid.uuid4)


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

            print(usuario.contrasena)
            print(usuario.contrasena.contrasena)
            print(usuario.contrasena.salt)

            repository = self.repository_factory.create(UsuarioRepository.__class__)
            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()

            UnitOfWorkPort.register_batch(uowf, repository.append, usuario)
            UnitOfWorkPort.commit(uowf)

        except BusinessRuleException as be:
            raise UnprocessableEntityError(str(be))
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError()


@execute_command.register(CreateUsuario)
def command_crear_usuario(command: CreateUsuario):
    CreateUsuarioHandler().handle(command)
