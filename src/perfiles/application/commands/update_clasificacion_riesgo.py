import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from perfiles.application.dtos import PerfilDemograficoDTO
from perfiles.application.exceptions import BadRequestError, UnprocessableEntityError
from perfiles.application.mappers import (
    PerfilDemograficoDTOEntityMapper,
)
from perfiles.application.queries.base import PerfilQueryBaseHandler
from perfiles.domain.entities import (
    PerfilDemografico,
)
from perfiles.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory
from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError


@dataclass
class ActualizarClasificacionRiesgo(Command):
    perfil_dto: PerfilDemograficoDTO = field(default_factory=PerfilDemograficoDTO)


class ActualizarClasificacionRiesgoHandler(PerfilQueryBaseHandler):

    def handle(self, command: ActualizarClasificacionRiesgo):
        uowf = None
        try:
            perfil_demografico: PerfilDemografico = self.perfiles_factory.create(
                command.perfil_dto, PerfilDemograficoDTOEntityMapper()
            )
            perfil_demografico.update(command.correlation_id)

            repository = self.repository_factory.create(PerfilDemografico)
            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()

            UnitOfWorkPort.register_batch(uowf, repository.update, perfil_demografico)
            UnitOfWorkPort.commit(uowf)

        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="perfiles.init.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="perfiles.error.internal")


@execute_command.register(ActualizarClasificacionRiesgo)
def command_crear_perfil_demografico(command: ActualizarClasificacionRiesgo):
    ActualizarClasificacionRiesgoHandler().handle(command)
