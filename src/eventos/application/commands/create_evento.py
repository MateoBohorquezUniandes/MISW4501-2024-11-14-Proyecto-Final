import traceback
from dataclasses import dataclass, field
from sqlalchemy.exc import IntegrityError

from eventos.application.dtos import EventoDTO
from eventos.domain.entities import Evento
from eventos.application.commands.base import EventoCommandBaseHandler
from eventos.application.mappers import EventoDTOEntityMapper
from eventos.infrastructure.uow import UnitOfWorkASQLAlchemyFactory
from eventos.application.exceptions import BadRequestError, UnprocessableEntityError

from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError


@dataclass
class CreateEvento(Command):
    evento_dto: EventoDTO = field(default_factory=EventoDTO)


class CreateEventoHandler(EventoCommandBaseHandler):
    def handle(self, command: CreateEvento):
        uowf = None
        try:
            evento: Evento = self._eventos_factory.create(
                command.evento_dto, EventoDTOEntityMapper()
            )

            repository = self.repository_factory.create(evento)

            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()

            UnitOfWorkPort.register_batch(uowf, repository.append, evento)
            UnitOfWorkPort.commit(uowf)
        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="evento.create.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="evento.error.internal")


@execute_command.register(CreateEvento)
def command_crear_evento(command: CreateEvento):
    CreateEventoHandler().handle(command)
