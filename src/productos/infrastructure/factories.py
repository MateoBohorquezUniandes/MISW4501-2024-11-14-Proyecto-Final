from dataclasses import dataclass
from productos.domain.entities import Producto
from productos.infrastructure.repositories import ProductoRepositoryPostgreSQL
from productos.infrastructure.exceptions import InvalidRepositoryFactoryException

from seedwork.domain.factories import Factory


@dataclass
class RepositoryFactory(Factory):
    def create(self, obj):
        if isinstance(obj, Producto) or obj == Producto:
            return ProductoRepositoryPostgreSQL()

        else:
            raise InvalidRepositoryFactoryException()
