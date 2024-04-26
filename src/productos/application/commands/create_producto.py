import traceback
from dataclasses import dataclass, field
from sqlalchemy.exc import IntegrityError

from productos.application.dtos import ProductoDTO
from productos.domain.entities import Producto
from productos.application.commands.base import ProductoCommandBaseHandler
from productos.application.mappers import ProductoDTOEntityMapper
from productos.infrastructure.uow import UnitOfWorkASQLAlchemyFactory
from productos.application.exceptions import BadRequestError, UnprocessableEntityError

from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError


@dataclass
class CreateProducto(Command):
    producto_dto: ProductoDTO = field(default_factory=ProductoDTO)


class CreateProductoHandler(ProductoCommandBaseHandler):
    def handle(self, command: CreateProducto):
        uowf = None
        try:
            producto: Producto = self._productos_factory.create(
                command.producto_dto, ProductoDTOEntityMapper()
            )

            repository = self.repository_factory.create(producto)

            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()

            UnitOfWorkPort.register_batch(uowf, repository.append, producto)
            UnitOfWorkPort.commit(uowf)
        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)
        except IntegrityError:
            traceback.print_exc()
            raise BadRequestError(code="producto.create.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="producto.error.internal")


@execute_command.register(CreateProducto)
def command_crear_producto(command: CreateProducto):
    CreateProductoHandler().handle(command)
