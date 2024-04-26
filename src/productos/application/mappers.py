from uuid import UUID

from productos.application.dtos import ProductoDTO
from productos.domain.entities import Producto

from seedwork.application.dtos import Mapper as ApplicationMapper
from seedwork.domain.repositories import Mapper as DomainMapper

# #####################################################################################
# Application Mappers
# #####################################################################################


class ProductoDTODictMapper(ApplicationMapper):
    def external_to_dto(self, external: dict) -> ProductoDTO:

        return ProductoDTO(
            tipo=external.get("tipo", ""),
            nombre=external.get("nombre", ""),
            descripcion=external.get("descripcion", ""),
            imagen=external.get("imagen", ""),
            precio=external.get("precio", ""),
            deporte=external.get("deporte", ""),
        )

    def dto_to_external(self, dto: ProductoDTO) -> dict:
        return dto.__dict__


# #####################################################################################
# Domain Mappers
# #####################################################################################


class ProductoDTOEntityMapper(DomainMapper):

    def type(self) -> type:
        return Producto

    def dto_to_entity(self, dto: ProductoDTO) -> Producto:

        args = [UUID(dto.id)] if dto.id else []
        producto = Producto(
            *args,
            tipo=dto.tipo,
            nombre=dto.nombre,
            imagen=dto.imagen,
            precio=dto.precio,
            descripcion=dto.descripcion,
            deporte=dto.deporte
        )
        return producto

    def entity_to_dto(self, entity: Producto) -> ProductoDTO:

        return ProductoDTO(
            entity.id,
            entity.tipo,
            entity.descripcion,
            entity.imagen,
            entity.precio,
            entity.nombre,
            entity.deporte,
        )
