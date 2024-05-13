import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from planes.application.commands.base import PlanCommandBaseHandler
from planes.application.dtos import RutinaRecuperacionDTO
from planes.application.exceptions import BadRequestError, UnprocessableEntityError
from planes.application.mappers import RutinaRecuperacionDTOEntityMapper
from planes.domain.entities import GrupoAlimenticio, RutinaRecuperacion
from planes.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory
from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError


@dataclass
class CreateRutinaRecuperacion(Command):
    rutina_dto: RutinaRecuperacionDTO = field(default_factory=RutinaRecuperacionDTO)


class CreateRutinaRecuperacionHandler(PlanCommandBaseHandler):
    def handle(self, command: CreateRutinaRecuperacion):
        uowf = None
        try:
            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()

            rutina: RutinaRecuperacion = self.planes_factory.create(
                command.rutina_dto, RutinaRecuperacionDTOEntityMapper()
            )
            repository_r = self.repository_factory.create(rutina)

            UnitOfWorkPort.register_batch(uowf, repository_r.append, rutina)
            UnitOfWorkPort.commit(uowf)

        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="rutinas.recuperacion.create.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="rutinas.recuperacion.error.internal")


@execute_command.register(CreateRutinaRecuperacion)
def command_crear_rutina_recuperacion(command: CreateRutinaRecuperacion):
    CreateRutinaRecuperacionHandler().handle(command)
