from dataclasses import dataclass, field
import datetime

from seedwork.application.dtos import DTO


@dataclass(frozen=True)
class ProductoDTO(DTO):
    id: str = field(default_factory=str)
    tipo: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    imagen: str = field(default_factory=str)
    precio: float = field(default_factory=float)
    nombre: str = field(default_factory=str)
    deporte: str = field(default_factory=str)
