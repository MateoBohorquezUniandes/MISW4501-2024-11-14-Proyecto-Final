import traceback
from dataclasses import dataclass, field

from seedwork.application.queries import Query, QueryResult, execute_query
from seedwork.presentation.exceptions import APIError

from productos.application.queries.base import ProductoQueryBaseHandler
from productos.domain.entities import Producto
from productos.application.mappers import ProductoDTOEntityMapper


class GetProductos(Query):

    def __init__(self, deporte=None, tipo=None):
        self.deporte = deporte
        self.tipo = tipo


class GetProductosQueryHandler(ProductoQueryBaseHandler):

    def handle(self, query: GetProductos) -> QueryResult:
        try:
            repository = self.repository_factory.create(Producto)
            productos: list[Producto] = repository.get_all(query.deporte, query.tipo)

            mapper = ProductoDTOEntityMapper()
            productos_dto = [
                self.productos_factory.create(e, mapper) for e in productos
            ]
            return QueryResult(result=productos_dto)

        except Exception as e:
            traceback.print_exc()
            raise APIError(message=str(e), code="productos.get.error.internal")


@execute_query.register(GetProductos)
def execute_query_productos(query: GetProductos):
    return GetProductosQueryHandler().handle(query)
