import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from perfiles.application.commands.base import PerfilCommandBaseHandler
from perfiles.application.dtos import MolestiaDTO
from perfiles.application.exceptions import BadRequestError, UnprocessableEntityError
from perfiles.application.mappers import MolestiaDTOEntityMapper
from perfiles.domain.entities import Molestia
from perfiles.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory
from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError


@dataclass
class CrearMolestia(Command):
    molestia_dto: MolestiaDTO = field(default_factory=MolestiaDTO)


class CrearMolestiaHandler(PerfilCommandBaseHandler):
    def handle(self, command: Command):
        uowf = None
        try:
            molestia: Molestia = self.perfiles_factory.create(
                command.molestia_dto, MolestiaDTOEntityMapper()
            )
            repository_molestias = self.repository_factory.create(molestia)

            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()
            UnitOfWorkPort.register_batch(uowf, repository_molestias.append, molestia)
            UnitOfWorkPort.commit(uowf)
        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="molestias.init.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="molestias.error.internal")


@execute_command.register(CrearMolestia)
def command_crear_molestia(command: CrearMolestia):
    CrearMolestiaHandler().handle(command)
