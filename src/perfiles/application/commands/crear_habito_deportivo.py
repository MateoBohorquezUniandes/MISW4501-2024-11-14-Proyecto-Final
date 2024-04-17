import traceback
import uuid
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError
from perfiles.application.commands.base import PerfilCommandBaseHandler
from perfiles.application.dtos import HabitoDeportivoDTO
from perfiles.domain.entities import HabitoDeportivo
from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from perfiles.application.exceptions import (
    UnprocessableEntityError,
    BadRequestError,
)
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError

from perfiles.application.mappers import HabitoDTOEntityMapper
from perfiles.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory


@dataclass
class CrearHabitoDeportivo(Command):
    habito_dto: HabitoDeportivoDTO = field(
        default_factory=HabitoDeportivoDTO
    )

class CrearHabitoDeportivoHandler(PerfilCommandBaseHandler):
    def handle(self, command: Command):
        uowf = None
        try:
            habito: HabitoDeportivo = self.perfiles_factory.create(
                command.habito_dto, HabitoDTOEntityMapper()
            )
            repository_habitos = self.repository_factory.create(habito)

            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()
            UnitOfWorkPort.register_batch(uowf, repository_habitos.append, habito)
            UnitOfWorkPort.commit(uowf)
        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="perfiles.init.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="habito.error.internal")

@execute_command.register(CrearHabitoDeportivo)
def command_crear_habito_deportivo(command: CrearHabitoDeportivo):
    CrearHabitoDeportivoHandler().handle(command)
