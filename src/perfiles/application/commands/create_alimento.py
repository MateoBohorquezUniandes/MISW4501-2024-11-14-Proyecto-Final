import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from perfiles.application.commands.base import PerfilCommandBaseHandler
from perfiles.application.dtos import AlimentoDTO
from perfiles.application.exceptions import BadRequestError, UnprocessableEntityError
from perfiles.application.mappers import AlimentoDTOEntityMapper
from perfiles.domain.entities import Alimento
from perfiles.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory
from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError


@dataclass
class CreateAlimento(Command):
    alimento_dto: AlimentoDTO = field(default_factory=AlimentoDTO)


class CreateAlimentoHandler(PerfilCommandBaseHandler):

    def handle(self, command: CreateAlimento):
        uowf = None
        try:
            alimento: Alimento = self.perfiles_factory.create(
                command.alimento_dto, AlimentoDTOEntityMapper()
            )

            repository = self.repository_factory.create(alimento)
            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()

            UnitOfWorkPort.register_batch(uowf, repository.append, alimento)
            UnitOfWorkPort.commit(uowf)

        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="alimentos.init.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="alimentos.error.internal")


@execute_command.register(CreateAlimento)
def command_crear_alimento(command: CreateAlimento):
    CreateAlimentoHandler().handle(command)
