from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from seedwork.domain.value_objects import ValueObject


@dataclass(frozen=True)
class InformacionDemografica(ValueObject):
    ubicacion: str


@dataclass(frozen=True)
class InformacionFisiologica(ValueObject):
    edad: int
    estatura: float
    peso: float


class CategoriaRiesgo(str, Enum):
    MUY_BAJA = "Muy Bajo"
    BAJA = "Bajo"
    MODERADA = "Moderado"
    ALTA = "Alto"
    MUY_ALTA = "Muy Alto"


class CategoriaIMC(str, Enum):
    BAJO_PESO = "Bajo Peso"
    PESO_NORMAL = "Peso Normal"
    SOBRE_PESO = "Sobre Peso"
    OBESIDAD = "Obesidad"
    OBESIDAD_MORBIDA = "Obesidad Morbiuda"


@dataclass(frozen=True)
class IndiceMasaCorporal(ValueObject):
    valor: float = field(default_factory=CategoriaIMC)
    categoria: CategoriaIMC = field(default_factory=CategoriaIMC)


@dataclass(frozen=True)
class ClasificacionRiesgo(ValueObject):
    imc: IndiceMasaCorporal
    riesgo: CategoriaRiesgo


class ExamenSanguineo(str, Enum):
    GLUCOSA = "Glucosa"
    UREA = "Urea"
    CREATININA = "Creatinina"
    ACIDO_URICO = "Acido Urico"
    COLESTEROL = "Colesterol"
    TRIGLICERIDOS = "Trigliceridos"


@dataclass(frozen=True)
class ResultadoElementoSanguineo(ValueObject):
    tipo_examen: ExamenSanguineo = field(default_factory=ExamenSanguineo)
    valor: float = field(default_factory=float)
    unidad: str = field(default_factory=str)


class TipoActividadDeportiva(str, Enum):
    AEROBICO = "Aerobico o Resistencia"
    ANAEROBICO = "Anaerobico o Fuerza"
    FUNCIONAL = "Funcional"
    HIIT = "Intervalos de Alta Intensidad"
    POTENCIA = "Potencia"


class FrecuenciaActividadDeportiva(str, Enum): ...


class TipoAlimentacion(str, Enum): ...
