import traceback
import uuid
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from planes.application.commands.base import PlanCommandBaseHandler
from planes.application.dtos import PlanEntrenamientoDTO
from planes.application.exceptions import BadRequestError, UnprocessableEntityError
from planes.application.mappers import PlanEntrenamientoDTOEntityMapper
from planes.domain.entities import PlanEntrenamiento
from planes.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory
from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError


@dataclass
class AsociarEntrenamientos(Command):
    plan_dto: PlanEntrenamientoDTO = field(default_factory=PlanEntrenamientoDTO)


class AsociarEntrenamientosHandler(PlanCommandBaseHandler):
    def handle(self, command: AsociarEntrenamientos):
        uowf = None
        try:
            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()
            repository_p = self.repository_factory.create(PlanEntrenamiento)

            plan = PlanEntrenamientoDTOEntityMapper().dto_to_entity(command.plan_dto)
            UnitOfWorkPort.register_batch(uowf, repository_p.update, plan)
            UnitOfWorkPort.commit(uowf)

        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="planes.create.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="planes.error.internal")


@execute_command.register(AsociarEntrenamientos)
def command_asociar_entrenamientos_a_plan(command: AsociarEntrenamientos):
    AsociarEntrenamientosHandler().handle(command)
