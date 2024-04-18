import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from seedwork.application.commands import Command, CommandResult, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError
from sesiones.application.commands.base import SesionCommandBaseHandler
from sesiones.application.dtos import SesionDeportivaDTO
from sesiones.application.exceptions import BadRequestError, UnprocessableEntityError
from sesiones.application.mappers import SesionDeportivaDTOEntityMapper
from sesiones.domain.entities import SesionDeportiva
from sesiones.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory


@dataclass
class CreateSesionDeportiva(Command):
    sesion_dto: SesionDeportivaDTO = field(default_factory=SesionDeportivaDTO)


class CreateSesionDeportivaHandler(SesionCommandBaseHandler):
    def handle(self, command: CreateSesionDeportiva):
        uowf = None
        try:
            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()

            mapper = SesionDeportivaDTOEntityMapper()
            sesion: SesionDeportiva = self.sesiones_factory.create(
                command.sesion_dto,
            )
            sesion.create(command.correlation_id)
            
            repository_p = self.repository_factory.create(sesion)
            UnitOfWorkPort.register_batch(uowf, repository_p.append, sesion)
            UnitOfWorkPort.commit(uowf)

            return CommandResult(self.sesiones_factory.create(sesion, mapper))

        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="sesiones.create.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="sesiones.error.internal")


@execute_command.register(CreateSesionDeportiva)
def command_crear_sesion(command: CreateSesionDeportiva):
    CreateSesionDeportivaHandler().handle(command)
