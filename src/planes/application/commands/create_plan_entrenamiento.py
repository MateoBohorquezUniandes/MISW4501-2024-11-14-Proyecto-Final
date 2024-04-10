import uuid
import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from planes.application.commands.base import PlanCommandBaseHandler
from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError
from planes.application.dtos import PlanEntrenamientoDTO
from planes.application.exceptions import (
    UnprocessableEntityError,
    BadRequestError,
)
from planes.application.mappers import (
    PlanEntrenamientoDTOEntityMapper,
)
from planes.domain.entities import (
    PlanEntrenamiento,
)
from planes.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory


@dataclass
class CreatePlanEntrenamiento(Command):
    plan_entrenamiento_dto: PlanEntrenamientoDTO = field(
        default_factory=PlanEntrenamientoDTO
    )


class CreatePlanEntrenamientoHandler(PlanCommandBaseHandler):
    def handle(self, command: CreatePlanEntrenamiento):
        uowf = None
        try:
            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()

            plan_entrenamiento: PlanEntrenamiento = self.planes_factory.create(
                command.plan_entrenamiento_dto, PlanEntrenamientoDTOEntityMapper()
            )
            plan_entrenamiento.create(command.correlation_id)
            repository_p = self.repository_factory.create(plan_entrenamiento)
            
            UnitOfWorkPort.register_batch(uowf, repository_p.append, plan_entrenamiento)
            UnitOfWorkPort.commit(uowf)

            if plan_entrenamiento.entrenamientos:
                repository_e = self.repository_factory.create(
                    plan_entrenamiento.entrenamientos[0]
                )
                entrenamientos_dto = repository_e.get_all(
                    ids=[e.id for e in plan_entrenamiento.entrenamientos],
                    as_entity=False,
                )
                UnitOfWorkPort.register_batch(
                    uowf, repository_p.update, plan_entrenamiento, entrenamientos_dto
                )
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


@execute_command.register(CreatePlanEntrenamiento)
def command_crear_plan_entrenamiento(command: CreatePlanEntrenamiento):
    CreatePlanEntrenamientoHandler().handle(command)