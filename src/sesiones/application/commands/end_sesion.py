import traceback
from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from seedwork.application.commands import Command, execute_command
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
class EndSesionDeportiva(Command):
    sesion_dto: SesionDeportivaDTO = field(default_factory=SesionDeportivaDTO)
    parameters: dict = field(default_factory=dict)


class EndSesionDeportivaHandler(SesionCommandBaseHandler):
    def handle(self, command: EndSesionDeportiva):
        uowf = None
        try:
            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()

            sesion: SesionDeportiva = self.sesiones_factory.create(
                command.sesion_dto, SesionDeportivaDTOEntityMapper()
            )
            sesion.completed_at = datetime.utcnow()
            sesion.end(command.correlation_id, command.parameters)

            repository_p = self.repository_factory.create(sesion)
            UnitOfWorkPort.register_batch(uowf, repository_p.update, sesion)
            UnitOfWorkPort.commit(uowf)

        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="sesiones.update.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="sesiones.error.internal")


@execute_command.register(EndSesionDeportiva)
def command_end_sesion(command: EndSesionDeportiva):
    EndSesionDeportivaHandler().handle(command)
