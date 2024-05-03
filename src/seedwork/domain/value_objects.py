from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class ValueObject: ...


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class GENERO(ExtendedEnum):
    MASCULINO = "M"
    FEMENINO = "F"
    OTRO = "O"


class TIPO_ALIMENTACION(ExtendedEnum):
    CARNIVORO = "Carnivoro"
    OMNIVORO = "Omnivoro"
    VEGETARIANO = "Vegetariano"
    VEGANO = "Vegano"

class CATEGORIA_ALIMENTO(ExtendedEnum):
    CARBOHIDRATO = "Carbohidrato"
    LIPIDO = "Lipido"
    LACTEO = "Lacteo"
    FRUTA = "Fruta"
    VERDURA = "Verdura"
    PROTEINA = "Proteina"
