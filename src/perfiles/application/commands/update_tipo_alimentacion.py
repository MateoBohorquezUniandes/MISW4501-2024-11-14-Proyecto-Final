import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from perfiles.application.commands.base import PerfilCommandBaseHandler
from perfiles.application.dtos import PerfilAlimenticioDTO
from perfiles.application.exceptions import BadRequestError, UnprocessableEntityError
from perfiles.application.mappers import (
    PerfilAlimenticioDTOEntityMapper,
)
from perfiles.domain.entities import (
    PerfilAlimenticio,
)
from perfiles.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory
from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError


@dataclass
class ActualizarTipoAlimentacion(Command):
    perfil_dto: PerfilAlimenticioDTO = field(default_factory=PerfilAlimenticioDTO)


class ActualizarTipoAlimentacionHandler(PerfilCommandBaseHandler):

    def handle(self, command: ActualizarTipoAlimentacion):
        uowf = None
        try:
            perfil: PerfilAlimenticio = self.perfiles_factory.create(
                command.perfil_dto, PerfilAlimenticioDTOEntityMapper()
            )

            repository = self.repository_factory.create(PerfilAlimenticio)
            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()

            UnitOfWorkPort.register_batch(uowf, repository.update, perfil)
            UnitOfWorkPort.commit(uowf)

        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="perfiles.alimenticio.update.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="perfiles.alimenticio.error.internal")


@execute_command.register(ActualizarTipoAlimentacion)
def command_crear_perfil_demografico(command: ActualizarTipoAlimentacion):
    ActualizarTipoAlimentacionHandler().handle(command)
