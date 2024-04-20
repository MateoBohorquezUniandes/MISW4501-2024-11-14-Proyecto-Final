from perfiles.domain.entities import (
    HabitoDeportivo,
    PerfilDemografico,
    ReporteSanguineo,
)
from perfiles.domain.value_objects import (
    CategoriaIMC,
    CategoriaRiesgo,
    ClasificacionRiesgo,
    ExamenSanguineo,
    HabitoFrecuencia,
    IndiceMasaCorporal,
    InformacionDemografica,
    InformacionFisiologica,
    UnidadExamenSanguineo,
)
from seedwork.domain.rules import (
    BusinessRule,
    CompoundBusinessRule,
    ValidFloat,
    ValidInteger,
    ValidString,
)
from seedwork.domain.value_objects import GENERO


class _ValidUnidadExamenSanguineo(BusinessRule):
    unidad: str

    def __init__(self, unidad, message="la clasificacion es invalida"):
        super().__init__(unidad, "unidad")
        self.unidad = unidad

    def is_valid(self) -> bool:
        return self.unidad in UnidadExamenSanguineo.list()


class _ValidExamenSanguineo(BusinessRule):
    examen: str

    def __init__(self, examen, message="la clasificacion es invalida"):
        super().__init__(examen, "tipo")
        self.examen = examen

    def is_valid(self) -> bool:
        return self.categoria in ExamenSanguineo.list()


class ValidReporteSanguineo(CompoundBusinessRule):
    reporte: ReporteSanguineo

    def __init__(self, reporte: ReporteSanguineo, message="reporte sanguineo invalido"):
        self.reporte = reporte

        rules = [
            _ValidExamenSanguineo(self.reporte.resultado.tipo_examen),
            ValidFloat(self.reporte.resultado.valor, 0.0, None, "valor fuera de rango"),
            _ValidUnidadExamenSanguineo(self.reporte.resultado.unidad),
        ]
        super().__init__(message, rules, "reporte_sanguineo")


class _ValidCategoriaIMC(BusinessRule):
    categoria: str

    def __init__(self, categoria, message="la clasificacion es invalida"):
        super().__init__(message, "categoria")
        self.categoria = categoria

    def is_valid(self) -> bool:
        return self.categoria in CategoriaIMC.list()


class _ValidIndiceMasaCorporal(CompoundBusinessRule):
    imc: IndiceMasaCorporal

    def __init__(self, imc: IndiceMasaCorporal, message="IMC invalido"):
        self.imc = imc

        rules = [
            ValidFloat(self.imc.valor, 1.0, 50.0, "IMC fuera de rango", "valor"),
            _ValidCategoriaIMC(self.imc.categoria),
        ]
        super().__init__(message, rules, "imc")


class _ValidCategoriaRiesgo(BusinessRule):
    categoria: str

    def __init__(self, categoria, message="la clasificacion es invalida"):
        super().__init__(message, "riesgo")
        self.categoria = categoria

    def is_valid(self) -> bool:
        return self.categoria in CategoriaRiesgo.list()


class ValidClasificacionRiesgo(CompoundBusinessRule):
    clasificacion: ClasificacionRiesgo

    def __init__(
        self,
        clasificacion: ClasificacionRiesgo,
        message="clasificacion de riesgo invalida",
    ):
        self.clasificacion = clasificacion

        rules = [
            _ValidCategoriaRiesgo(self.clasificacion.riesgo),
            _ValidIndiceMasaCorporal(self.clasificacion.imc),
        ]
        super().__init__(message, rules, "fisiologia")


class ValidDemografia(CompoundBusinessRule):
    demografia: InformacionDemografica

    def __init__(
        self, demografia: InformacionDemografica, message="fisiologia invalida"
    ):
        self.demografia = demografia

        rules = [
            ValidString(self.demografia.pais, 2, 120, "pais invalido", "pais"),
            ValidString(self.demografia.ciudad, 2, 120, "ciudad invalida", "ciudad"),
        ]
        super().__init__(message, rules, "fisiologia")


class _ValidGenero(BusinessRule):
    genero: str

    def __init__(self, genero, message="El genero no es una opcion valida"):
        super().__init__(message, "genero")
        self.genero = genero

    def is_valid(self) -> bool:
        return self.genero in GENERO.list()


class ValidFisiologica(CompoundBusinessRule):
    fisiologia: InformacionFisiologica

    def __init__(
        self, fisiologia: InformacionFisiologica, message="fisiologia invalida"
    ):
        self.fisiologia = fisiologia

        rules = [
            _ValidGenero(self.fisiologia.genero),
            ValidInteger(self.fisiologia.edad, 18, 100, "edad fuera del rango", "edad"),
            ValidFloat(
                self.fisiologia.peso, 1.0, 300.0, "peso fuera del rango", "peso"
            ),
            ValidFloat(
                self.fisiologia.altura, 1.0, 3.0, "altura fuera del rango", "altura"
            ),
        ]
        super().__init__(message, rules, "fisiologia")


class ValidPerfilDemografico(CompoundBusinessRule):
    perfil: PerfilDemografico

    def __init__(self, perfil: PerfilDemografico, message="perfil invalida"):
        self.perfil: PerfilDemografico = perfil

        rules = [
            ValidString(
                self.perfil.tipo_identificacion, 2, 10, "tipo identificacion invalida"
            ),
            ValidString(self.perfil.identificacion, 2, 20, "identificacion invalida"),
            ValidClasificacionRiesgo(self.perfil.clasificacion_riesgo),
            ValidDemografia(self.perfil.demografia),
            ValidFisiologica(self.perfil.fisiologia),
        ]

        rules.extend(
            [ValidReporteSanguineo(rs) for rs in self.perfil.reportes_sanguineo]
        )

        super().__init__(message, rules, "perfil")


class _ValidHabitoFrecuencia(BusinessRule):
    habito: str

    def __init__(self, habito, message="El habito no es una opcion valida"):
        super().__init__(message, "habito")
        self.habito = habito

    def is_valid(self) -> bool:
        return self.habito in HabitoFrecuencia.list()


class ValidHabitoDeportivo(CompoundBusinessRule):
    habito: HabitoDeportivo

    def __init__(self, habito: HabitoDeportivo, message="habito invalido"):
        self.habito: HabitoDeportivo = habito

        rules = [
            ValidString(self.habito.titulo, 2, 50, "titulo invalido"),
            ValidString(self.habito.descripcion, 2, 400, "descipcion invalida"),
            _ValidHabitoFrecuencia(self.habito.frecuencia),
        ]

        super().__init__(message, rules, "habito")
