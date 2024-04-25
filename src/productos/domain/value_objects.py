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


class DEPORTE(ExtendedEnum):
    CILICMO = "Ciclismo"
    ATLETISMO = "Atletismo"


@dataclass(frozen=True)
class Imagen(ValueObject):
    url: str = field(default_factory=str)


@dataclass(frozen=True)
class ProductoTipo(ValueObject):
    tipo: ProductoTipoEnum = field(default_factory=ProductoTipoEnum)


@dataclass(frozen=True)
class ProductoDeporte(ValueObject):
    deporte: DEPORTE = field(default_factory=DEPORTE)
