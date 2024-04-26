from dataclasses import dataclass

from productos.domain.entities import Producto
from productos.domain.rules import ValidProducto
from productos.domain.exceptions import InvalidProductoFactoryException

from seedwork.domain.entities import Entity
from seedwork.domain.events import DomainEvent
from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Mapper


@dataclass
class _ProductoFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None) -> Producto:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)

        producto: Producto = mapper.dto_to_entity(obj)
        self.validate_rule(ValidProducto(producto))

        return producto


@dataclass
class ProductoFactoy(Factory):
    def create(self, obj: any, mapper: Mapper):
        if mapper.type() == Producto:
            producto_factory = _ProductoFactory()
            return producto_factory.create(obj, mapper)
        else:
            raise InvalidProductoFactoryException()
