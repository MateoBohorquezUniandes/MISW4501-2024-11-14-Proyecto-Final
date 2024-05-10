from productos.domain.entities import Producto
from productos.domain.value_objects import ProductoTipoEnum
from seedwork.domain.rules import BusinessRule, CompoundBusinessRule, ValidString
from seedwork.domain.value_objects import DEPORTE


class _ValidProductoTipo(BusinessRule):
    tipo: str

    def __init__(self, tipo, message="El tipo de producto no es una opcion valida"):
        super().__init__(message, "producto")
        self.tipo = tipo

    def is_valid(self) -> bool:
        return self.tipo in ProductoTipoEnum.list()


class _ValidProductoDeporte(BusinessRule):
    tipo: str

    def __init__(self, tipo, message="El deporte no es una opcion valida"):
        super().__init__(message, "producto")
        self.tipo = tipo

    def is_valid(self) -> bool:
        return self.tipo in DEPORTE.list()


class ValidProducto(CompoundBusinessRule):
    producto: Producto

    def __init__(self, producto: Producto, message="producto invalido"):
        self.producto: Producto = producto

        rules = [
            ValidString(self.producto.descripcion, 2, 400, "descripcion invalido"),
            ValidString(self.producto.nombre, 2, 100, "nombre invalido"),
            _ValidProductoTipo(self.producto.tipo),
            _ValidProductoDeporte(self.producto.deporte),
        ]

        super().__init__(message, rules, "producto")
