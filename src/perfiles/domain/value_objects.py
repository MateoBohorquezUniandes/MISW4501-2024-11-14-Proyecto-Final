from dataclasses import dataclass, field
from enum import Enum

from seedwork.domain.value_objects import ExtendedEnum, ValueObject


@dataclass(frozen=True)
class InformacionDemografica(ValueObject):
    pais: str = field(default_factory=str)
    ciudad: str = field(default_factory=str)


@dataclass(frozen=True)
class InformacionFisiologica(ValueObject):
    genero: str = field(default_factory=str)
    edad: int = field(default_factory=int)
    altura: float = field(default_factory=float)
    peso: float = field(default_factory=float)

    def calculate_imc(self):
        imc_value = round(self.peso / self.altura**2, ndigits=2)
        return IndiceMasaCorporal(imc_value, CategoriaIMC.get(imc_value))


class CategoriaRiesgo(ExtendedEnum):
    MUY_BAJA = "Muy Bajo"
    BAJA = "Bajo"
    MODERADA = "Moderado"
    ALTA = "Alto"
    MUY_ALTA = "Muy Alto"


class CategoriaIMC(str, ExtendedEnum):
    BAJO_PESO = "Bajo Peso"
    PESO_NORMAL = "Peso Normal"
    SOBRE_PESO = "Sobre Peso"
    OBESIDAD = "Obesidad 1"
    OBESIDAD_MORBIDA = "Obesidad Morbida"

    @classmethod
    def get(cls, valor):
        if valor <= 18.5:
            return cls.BAJO_PESO.value
        elif valor <= 24.9:
            return cls.PESO_NORMAL.value
        elif valor <= 29.9:
            return cls.SOBRE_PESO.value
        elif valor <= 34.9:
            return cls.OBESIDAD.value
        else:
            return cls.OBESIDAD_MORBIDA.value


@dataclass(frozen=True)
class IndiceMasaCorporal(ValueObject):
    valor: float = field(default_factory=float)
    categoria: CategoriaIMC = field(default=CategoriaIMC.PESO_NORMAL.value)


@dataclass(frozen=True)
class ClasificacionRiesgo(ValueObject):
    imc: IndiceMasaCorporal = field(default_factory=IndiceMasaCorporal)
    riesgo: CategoriaRiesgo = field(default=None, init=False)

    def __post_init__(self):
        riesgo = None
        if self.imc.categoria == CategoriaIMC.BAJO_PESO.value:
            riesgo = CategoriaRiesgo.MUY_BAJA.value
        elif self.imc.categoria == CategoriaIMC.PESO_NORMAL.value:
            riesgo = CategoriaRiesgo.BAJA.value
        elif self.imc.categoria == CategoriaIMC.SOBRE_PESO.value:
            riesgo = CategoriaRiesgo.MODERADA.value
        elif self.imc.categoria == CategoriaIMC.OBESIDAD.value:
            riesgo = CategoriaRiesgo.ALTA.value
        else:
            riesgo = CategoriaRiesgo.MUY_ALTA.value

        object.__setattr__(self, "riesgo", riesgo)


class ExamenSanguineo(ExtendedEnum):
    GLUCOSA = "Glucosa"
    UREA = "Urea"
    CREATININA = "Creatinina"
    ACIDO_URICO = "Acido Urico"
    COLESTEROL = "Colesterol"
    TRIGLICERIDOS = "Trigliceridos"


class UnidadExamenSanguineo(ExtendedEnum):
    MG_DL = "mg/dL"


@dataclass(frozen=True)
class ResultadoElementoSanguineo(ValueObject):
    tipo_examen: ExamenSanguineo = field(default_factory=ExamenSanguineo)
    valor: float = field(default_factory=float)
    unidad: UnidadExamenSanguineo = field(
        default_factory=UnidadExamenSanguineo.MG_DL.value
    )


class TipoActividadDeportiva(str, Enum):
    AEROBICO = "Aerobico o Resistencia"
    ANAEROBICO = "Anaerobico o Fuerza"
    FUNCIONAL = "Funcional"
    HIIT = "Intervalos de Alta Intensidad"
    POTENCIA = "Potencia"


class TipoAlimentacion(str, Enum): ...
