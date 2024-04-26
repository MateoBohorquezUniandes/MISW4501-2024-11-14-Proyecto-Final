import datetime

from uuid import UUID

from productos.domain.entities import Producto
from productos.infrastructure.dtos import Producto as ProductoDto

from seedwork.domain.repositories import Mapper


class ProductoMapper(Mapper):
    def type(self) -> type:
        return Producto

    def dto_to_entity(self, dto: ProductoDto) -> Producto:

        args = [UUID(dto.id)] if dto.id else []
        return Producto(
            *args,
            descripcion=dto.descripcion,
            imagen=dto.imagen,
            nombre=dto.nombre,
            precio=dto.precio,
            tipo=dto.tipo,
            deporte=dto.deporte
        )

    def entity_to_dto(self, entity: Producto) -> ProductoDto:
        producto_dto = ProductoDto()
        producto_dto.descripcion = entity.descripcion
        producto_dto.imagen = entity.imagen
        producto_dto.nombre = entity.nombre
        producto_dto.precio = entity.precio
        producto_dto.tipo = entity.tipo
        producto_dto.deporte = entity.deporte
        producto_dto.id = entity.id

        return producto_dto
