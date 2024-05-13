import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import NoResultFound

from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError
from usuarios.application.exceptions import (
    UnprocessableEntityError,
    UsuarioNotFoundError,
)
from usuarios.application.mappers import UsuarioDTOEntityMapper
from usuarios.application.queries.base import UsuarioBaseHandler
from usuarios.domain.entities import Usuario
from usuarios.domain.value_objects import ROL


@dataclass
class ObtenerUsuario(Query):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
    rol: ROL = field(default_factory=str)


class ObtenerUsuarioHandler(UsuarioBaseHandler):
    def handle(self, query: ObtenerUsuario):
        try:
            repository = self.repository_factory.create(query.rol)
            usuario: Usuario = repository.get(
                query.tipo_identificacion, query.identificacion
            )

            return QueryResult(
                result=self.usuarios_factory.create(usuario, UsuarioDTOEntityMapper())
            )

        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except NoResultFound:
            traceback.print_exc()
            raise UsuarioNotFoundError()
        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="users.get.error.internal")


@execute_query.register(ObtenerUsuario)
def command_crear_usuario(command: ObtenerUsuario):
    return ObtenerUsuarioHandler().handle(command)
