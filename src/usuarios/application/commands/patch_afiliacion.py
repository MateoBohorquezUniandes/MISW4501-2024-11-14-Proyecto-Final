import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError
from usuarios.application.commands.base import UsuarioBaseHandler
from usuarios.application.exceptions import BadRequestError, UnprocessableEntityError
from usuarios.domain.entities import Deportista
from usuarios.domain.exceptions import InvalidRolUsuarioError
from usuarios.domain.rules import ValidPlanAfiliacion
from usuarios.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory


@dataclass
class ActualizarAfiliacion(Command):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
    plan_afiliacion: str = field(default_factory=str)


class ActualizarAfiliacionHandler(UsuarioBaseHandler):
    def handle(self, command: ActualizarAfiliacion):
        uowf = None
        try:
            repository = self.repository_factory.create(Deportista)
            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()
            self.usuarios_factory.validate_rule(
                ValidPlanAfiliacion(command.plan_afiliacion)
            )

            UnitOfWorkPort.register_batch(
                uowf,
                repository.update,
                command.tipo_identificacion,
                command.identificacion,
                plan_afiliacion=command.plan_afiliacion,
            )
            UnitOfWorkPort.commit(uowf)

        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="user.afiliacionintegrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="user.afiliacion.error.internal")


@execute_command.register(ActualizarAfiliacion)
def command_crear_usuario(command: ActualizarAfiliacion):
    ActualizarAfiliacionHandler().handle(command)
