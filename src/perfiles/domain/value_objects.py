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


class CategoriaVOM(str, ExtendedEnum):
    MUY_POBRE = "Muy Pobre"
    POBRE = "Pobre"
    REGULAR = "Regular"
    BUENO = "Bueno"
    EXCELENTE = "Excelente"

    @classmethod
    def get(cls, valor: float, genero: str, edad: int):
        categorias = {
            "F": {
                19: [35.0, 38.4, 45.2, 51.0, 55.9],
                29: [33.0, 36.5, 42.5, 46.5, 52.4],
                39: [31.5, 35.5, 41.0, 45.0, 49.4],
                49: [30.2, 33.6, 39.0, 43.8, 48.0],
                59: [26.1, 31.0, 35.8, 41.0, 45.3],
                200: [20.5, 26.1, 32.3, 36.5, 44.2],
            },
            "M": {
                19: [25.0, 31.0, 35.0, 39.0, 42.0],
                29: [26.6, 29.0, 33.0, 37.0, 41.0],
                39: [22.8, 27.0, 31.5, 35.7, 40.0],
                49: [21.0, 24.5, 29.0, 32.9, 36.9],
                59: [20.2, 22.8, 27.0, 31.5, 35.7],
                200: [17.5, 20.2, 24.5, 30.3, 31.4],
            },
            "O": {
                19: [25.0, 31.0, 35.0, 39.0, 42.0],
                29: [26.6, 29.0, 33.0, 37.0, 41.0],
                39: [22.8, 27.0, 31.5, 35.7, 40.0],
                49: [21.0, 24.5, 29.0, 32.9, 36.9],
                59: [20.2, 22.8, 27.0, 31.5, 35.7],
                200: [17.5, 20.2, 24.5, 30.3, 31.4],
            },
        }
        rango = [next(v for i, v in categorias[genero].items() if i > edad)][0]
        return cls.list()[next(i for i, v in enumerate(rango) if v > valor)]


@dataclass(frozen=True)
class VolumenMaximoOxigeno(ValueObject):
    valor: float = field(default_factory=float)
    categoria: CategoriaVOM = field(default=CategoriaVOM.REGULAR.value)


@dataclass(frozen=True)
class ClasificacionRiesgo(ValueObject):
    imc: IndiceMasaCorporal = field(default_factory=IndiceMasaCorporal)
    riesgo: CategoriaRiesgo = field(default=None, init=False)
    vo_max: VolumenMaximoOxigeno = field(default_factory=VolumenMaximoOxigeno)

    def __post_init__(self):
        riesgo = None
        imcc = self.imc.categoria
        vomc = self.vo_max.categoria
        if any(
            [imcc == CategoriaIMC.BAJO_PESO.value, vomc == CategoriaVOM.EXCELENTE.value]
        ):
            riesgo = CategoriaRiesgo.MUY_BAJA.value
        elif any(
            [imcc == CategoriaIMC.PESO_NORMAL.value, vomc == CategoriaVOM.BUENO.value]
        ):
            riesgo = CategoriaRiesgo.BAJA.value
        elif any(
            [imcc == CategoriaIMC.SOBRE_PESO.value, vomc == CategoriaVOM.REGULAR.value]
        ):
            riesgo = CategoriaRiesgo.MODERADA.value
        elif any(
            [imcc == CategoriaIMC.OBESIDAD.value, vomc == CategoriaVOM.POBRE.value]
        ):
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


class HabitoFrecuencia(ExtendedEnum):
    DIARIO = "Diario"
    SEMANAL = "Semanal"
    MENSUAL = "Mensual"
    ANUAL = "Anual"


@dataclass(frozen=True)
class HabitoDeportivoFrecuencia(ValueObject):
    frecuencia: HabitoFrecuencia = field(default_factory=HabitoFrecuencia)


class MolestiaTipoEnum(ExtendedEnum):
    MOLESTIA = "Molestia"
    LESION = "Lesion"
    INCAPACIDAD = "Incapacidad"


@dataclass(frozen=True)
class MolestiaTipo(ValueObject):
    tipo: MolestiaTipoEnum = field(default_factory=MolestiaTipoEnum)
