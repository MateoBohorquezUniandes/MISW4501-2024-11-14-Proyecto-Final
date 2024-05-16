from dataclasses import dataclass, field
from sqlite3 import IntegrityError
import traceback
from perfiles.application.commands.base import PerfilCommandBaseHandler
from perfiles.application.dtos import ReporteSanguineoDTO
from perfiles.application.exceptions import BadRequestError, UnprocessableEntityError
from perfiles.application.mappers import ReporteSanguineoDTOEntityMapper
from perfiles.domain.entities import ReporteSanguineo
from perfiles.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory
from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError


@dataclass
class AssociateReporteSanguineo(Command):
    reporte_sanguineo_dto: ReporteSanguineoDTO = field(
        default_factory=ReporteSanguineoDTO
    )
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)


class AssociateReporteSanguineoHandler(PerfilCommandBaseHandler):

    def handle(self, command: AssociateReporteSanguineo):
        uowf = None
        try:
            reporte_sanguineo: ReporteSanguineo = self.perfiles_factory.create(
                command.reporte_sanguineo_dto,
                ReporteSanguineoDTOEntityMapper(),
                tipo_identificacion=command.tipo_identificacion,
                identificacion=command.identificacion,
            )

            repository = self.repository_factory.create(reporte_sanguineo)
            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()

            UnitOfWorkPort.register_batch(uowf, repository.append, reporte_sanguineo)
            UnitOfWorkPort.commit(uowf)

        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="reporte_sanguineo.init.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="reporte_sanguineo.error.internal")


@execute_command.register(AssociateReporteSanguineo)
def command_crear_reporte_sanguineo(command: AssociateReporteSanguineo):
    AssociateReporteSanguineoHandler().handle(command)
