import productos.domain.value_objects as vo
from dataclasses import asdict, dataclass, field

from seedwork.domain.entities import Entity, RootAggregation


@dataclass
class Producto(RootAggregation):
    tipo: vo.ProductoTipo = field(default_factory=vo.ProductoTipo)
    descripcion: str = field(default_factory=str)
    imagen: vo.Imagen = field(default_factory=vo.Imagen)
    precio: float = field(default_factory=float)
    nombre: str = field(default_factory=str)
    deporte: vo.ProductoDeporte = field(default_factory=vo.ProductoDeporte)
