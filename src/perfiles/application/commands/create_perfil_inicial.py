import uuid
import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError
from perfiles.application.commands.base import UsuarioBaseHandler
from perfiles.application.dtos import PerfilDemograficoDTO
from perfiles.application.exceptions import (
    UnprocessableEntityError,
    BadRequestError,
)
from perfiles.application.mappers import (
    PerfilAlimenticioInitialEntityMapper,
    PerfilDemograficoDTOEntityMapper,
    PerfilDeportivoInitialEntityMapper,
)
from perfiles.domain.entities import (
    PerfilDemografico,
    PerfilDeportivo,
    PerfilAlimenticio,
)
from perfiles.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory


@dataclass
class PerfilamientoInicial(Command):
    perfiles_demografico_dto: PerfilDemograficoDTO
    correlation_id: uuid.UUID = field(default_factory=uuid.uuid4)


class CreatePerfilInicialHandler(PerfilCommandBaseHandler):

    def handle(self, command: PerfilamientoInicial):
        uowf = None
        try:
            perfil_demografico: PerfilDemografico = self.perfiles_factory.create(
                command.perfiles_demografico_dto, PerfilDemograficoDTOEntityMapper()
            )
            perfil_demografico.create(command.correlation_id)
            repository_pdm = self.repository_factory.create(perfil_demografico)

            perfi_deportivo: PerfilDeportivo = self.perfiles_factory.create(
                command.perfiles_demografico_dto, PerfilDeportivoInitialEntityMapper()
            )
            repository_pdp = self.repository_factory.create(perfi_deportivo)

            perfi_alimenticio: PerfilAlimenticio = self.perfiles_factory.create(
                command.perfiles_demografico_dto, PerfilAlimenticioInitialEntityMapper()
            )
            repository_am = self.repository_factory.create(perfi_alimenticio)

            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()

            UnitOfWorkPort.register_batch(
                uowf, repository_pdm.append, perfil_demografico
            )
            UnitOfWorkPort.register_batch(uowf, repository_pdp.append, perfi_deportivo)
            UnitOfWorkPort.register_batch(uowf, repository_am.append, perfi_alimenticio)
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


@execute_command.register(PerfilamientoInicial)
def command_crear_perfil_demografico(command: PerfilamientoInicial):
    CreatePerfilInicialHandler().handle(command)
