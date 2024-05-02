import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from planes.application.commands.base import PlanCommandBaseHandler
from planes.application.dtos import RutinaAlimentacionDTO
from planes.application.exceptions import BadRequestError, UnprocessableEntityError
from planes.application.mappers import RutinaAlimentacionDTOEntityMapper
from planes.domain.entities import GrupoAlimenticio, RutinaAlimentacion
from planes.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory
from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError


@dataclass
class CreateRutinaAlimentacion(Command):
    rutina_dto: RutinaAlimentacionDTO = field(default_factory=RutinaAlimentacionDTO)


class CreateRutinaAlimentacionHandler(PlanCommandBaseHandler):
    def handle(self, command: CreateRutinaAlimentacion):
        uowf = None
        try:
            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()

            rutina: RutinaAlimentacion = self.planes_factory.create(
                command.rutina_dto, RutinaAlimentacionDTOEntityMapper()
            )
            repository_r = self.repository_factory.create(rutina)

            UnitOfWorkPort.register_batch(uowf, repository_r.append, rutina)

            repository_g = self.repository_factory.create(GrupoAlimenticio)
            for grupo in rutina.grupos_alimenticios:
                UnitOfWorkPort.register_batch(
                    uowf, repository_g.append, grupo, str(rutina.id)
                )
            UnitOfWorkPort.commit(uowf)

        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="rutinas.alimentation.create.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="rutinas.alimentation.error.internal")


@execute_command.register(CreateRutinaAlimentacion)
def command_crear_rutina(command: CreateRutinaAlimentacion):
    CreateRutinaAlimentacionHandler().handle(command)
