import uuid
import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from planes.application.commands.base import PlanCommandBaseHandler
from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError
from planes.application.dtos import EntrenamientoDTO
from planes.application.exceptions import (
    UnprocessableEntityError,
    BadRequestError,
)
from planes.application.mappers import (
    EntrenamientoDTOEntityMapper,
)
from planes.domain.entities import (
    Entrenamiento,
)
from planes.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory


@dataclass
class CreateEntrenamiento(Command):
    entrenamiento_dto: EntrenamientoDTO = field(default_factory=EntrenamientoDTO)


class CreateEntrenamientoHandler(PlanCommandBaseHandler):
    def handle(self, command: CreateEntrenamiento):
        uowf = None
        try:
            entrenamiento: Entrenamiento = self.planes_factory.create(
                command.entrenamiento_dto, EntrenamientoDTOEntityMapper()
            )
            entrenamiento.create(command.correlation_id)
            repository = self.repository_factory.create(entrenamiento)

            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()

            UnitOfWorkPort.register_batch(uowf, repository.append, entrenamiento)
            UnitOfWorkPort.commit(uowf)
        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="entrenamientos.create.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="entrenamientos.error.internal")


@execute_command.register(CreateEntrenamiento)
def command_crear_entrenamiento(command: CreateEntrenamiento):
    CreateEntrenamientoHandler().handle(command)
