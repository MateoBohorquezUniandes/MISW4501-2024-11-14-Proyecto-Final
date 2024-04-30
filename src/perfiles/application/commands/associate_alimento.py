import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from perfiles.application.commands.base import PerfilCommandBaseHandler
from perfiles.application.dtos import AlimentoDTO
from perfiles.application.exceptions import BadRequestError, UnprocessableEntityError
from perfiles.application.mappers import (
    AlimentoAsociadoDTOEntityMapper,
)
from perfiles.domain.value_objects import AlimentoAsociado
from perfiles.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory
from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError


@dataclass
class AssociateAlimento(Command):
    alimento_dto: AlimentoDTO = field(default_factory=AlimentoDTO)
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)


class AssociateAlimentoHandler(PerfilCommandBaseHandler):

    def handle(self, command: AssociateAlimento):
        uowf = None
        try:
            asociacion: AlimentoAsociado = self.perfiles_factory.create(
                command.alimento_dto,
                AlimentoAsociadoDTOEntityMapper(),
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
            raise BadRequestError(code="alimentos.init.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="alimentos.error.internal")


@execute_command.register(AssociateAlimento)
def command_crear_alimento(command: AssociateAlimento):
    AssociateAlimentoHandler().handle(command)
