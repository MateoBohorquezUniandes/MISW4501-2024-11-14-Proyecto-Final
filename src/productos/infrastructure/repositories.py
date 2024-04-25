from typing import Union

from productos.domain.repositories import ProductoRepository
from productos.domain.factories import ProductoFactoy
from productos.domain.entities import Producto
from productos.infrastructure.dtos import Producto as ProductoDto
from productos.infrastructure.mappers import ProductoMapper
from productos.infrastructure.db import db


class ProductoRepositoryPostgreSQL(ProductoRepository):
    def __init__(self):
        self.producto_factory: ProductoFactoy = ProductoFactoy()

    @property
    def fabrica_producto_factory(self):
        return self.producto_factory

    def get_all(
        self, deporte: str = None, tipo: str = None, as_entity=True
    ) -> Union[list[Producto], list[ProductoDto]]:
        query = db.session.query(ProductoDto)

        if tipo:
            query = query.filter_by(tipo=tipo)
        if deporte:
            query = query.filter_by(deporte=deporte)

        productos_dto = query.all()
        return (
            [
                self.producto_factory.create(dto, ProductoMapper())
                for dto in productos_dto
            ]
            if as_entity
            else productos_dto
        )

    def get(self) -> Producto:
        pass

    def append(self, producto: Producto):
        producto_dto = self.producto_factory.create(producto, ProductoMapper())
        db.session.add(producto_dto)

    def delete(self):
        pass

    def update(self):
        pass
