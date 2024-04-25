from dataclasses import dataclass, field
from enum import Enum

from seedwork.domain.value_objects import ExtendedEnum, ValueObject


class ProductoTipoEnum(str, ExtendedEnum):
    ALIMENTACION = "Alimentacion"
    TRANSPORTE = "Transporte"
    MECANICOS = "Mecanicos"
    MEDICOS = "Medicos"
    ENTRENADORES = "Entrenadores"
    ELEMENTOS_DEPORTIVOS = "Elementos Deportivos"
    MANTENIMIENTO = "Mantenimiento"
    LAVADO = "Lavado"


@dataclass(frozen=True)
class Imagen(ValueObject):
    url: str = field(default_factory=str)


@dataclass(frozen=True)
class ProductoTipo(ValueObject):
    tipo: ProductoTipoEnum = field(default_factory=ProductoTipoEnum)
