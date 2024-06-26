import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from planes.application.commands.base import PlanCommandBaseHandler
from planes.application.dtos import ObjetivoEntrenamientoDTO, UsuarioPlanDTO
from planes.application.exceptions import BadRequestError, UnprocessableEntityError
from planes.application.mappers import (
    ObjetivoEntrenamientoDTOEntityMapper,
    UsuarioPlanDTOEntityMapper,
)
from planes.domain.entities import UsuarioPlan
from planes.domain.value_objects import ObjetivoEntrenamiento
from planes.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory
from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError


@dataclass
class CreateRecomendacionPlan(Command):
    usuario_dto: UsuarioPlanDTO = field(default_factory=UsuarioPlanDTO)
    objetivo_dto: ObjetivoEntrenamientoDTO = field(
        default_factory=ObjetivoEntrenamientoDTO
    )


class CreateRecomendacionPlanHandler(PlanCommandBaseHandler):
    def handle(self, command: CreateRecomendacionPlan):
        uowf = None
        try:
            objetivo: ObjetivoEntrenamiento = self.planes_factory.create(
                command.objetivo_dto, ObjetivoEntrenamientoDTOEntityMapper()
            )
            usuario: UsuarioPlan = self.planes_factory.create(
                command.usuario_dto, UsuarioPlanDTOEntityMapper()
            )
            usuario.create(command.correlation_id)
            repository_u = self.repository_factory.create(usuario)

            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()
            UnitOfWorkPort.register_batch(
                uowf,
                repository_u.append,
                usuario,
                objetivo.deporte,
                objetivo.exigencia,
            )

            UnitOfWorkPort.commit(uowf)

        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="usuarios_plan.recommend.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="usuarios_plan.error.internal")


@execute_command.register(CreateRecomendacionPlan)
def command_crear_recomendacion(command: CreateRecomendacionPlan):
    CreateRecomendacionPlanHandler().handle(command)
