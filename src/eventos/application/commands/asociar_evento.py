import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from eventos.application.commands.base import EventoCommandBaseHandler
from eventos.application.dtos import EventoDTO
from eventos.application.exceptions import BadRequestError, UnprocessableEntityError
from eventos.application.mappers import (
    EventoAsociadoDTOEntityMapper,
)
from eventos.domain.value_objects import EventoAsociado
from eventos.infrastructure.uow import UnitOfWorkASQLAlchemyFactory
from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError


@dataclass
class AssociateEvento(Command):
    evento_dto: EventoDTO = field(default_factory=EventoDTO)
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)


class AssociateEventoHandler(EventoCommandBaseHandler):

    def handle(self, command: AssociateEvento):
        uowf = None
        try:
            asociacion: EventoAsociado = self.eventos_factory.create(
                command.evento_dto,
                EventoAsociadoDTOEntityMapper(),
                tipo_identificacion=command.tipo_identificacion,
                identificacion=command.identificacion,
            )

            repository = self.repository_factory.create(asociacion)
            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()

            UnitOfWorkPort.register_batch(uowf, repository.append, asociacion)
            UnitOfWorkPort.commit(uowf)

        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="eventos.asociados.init.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="eventos.asociados.error.internal")


@execute_command.register(AssociateEvento)
def command_crear_evento(command: AssociateEvento):
    AssociateEventoHandler().handle(command)
