from planes.domain.entities import Entrenamiento, PlanEntrenamiento, UsuarioPlan
from seedwork.domain.rules import (
    BusinessRule,
    CompoundBusinessRule,
    ValidFloat,
    ValidInteger,
    ValidString,
)
from planes.domain.value_objects import (
    DEPORTE,
    DURACION_UNIDAD,
    EXIGENCIA,
    PLAN_CATEGORIA,
    ObjetivoEntrenamiento,
)


class _ValidDuracionunidad(BusinessRule):
    unidad: str

    def __init__(self, unidad, message="El unidad no es una opcion valida"):
        super().__init__(message, "unidad")
        self.unidad = unidad

    def is_valid(self) -> bool:
        return self.unidad in DURACION_UNIDAD.list()


class ValidEntrenamiento(CompoundBusinessRule):
    entrenamiento: Entrenamiento

    def __init__(self, entrenamiento: Entrenamiento, message="entrenamiento invalido"):
        self.entrenamiento: Entrenamiento = entrenamiento

        rules = [
            ValidString(self.entrenamiento.nombre, 2, 120, "nombre invalido", "nombre"),
            ValidString(
                self.entrenamiento.grupo_muscular,
                2,
                50,
                "grupo muscular invalido",
                "grupo_muscular",
            ),
            ValidString(
                self.entrenamiento.descripcion,
                2,
                400,
                "descripcion invalida",
                "descripcion",
            ),
            ValidInteger(
                self.entrenamiento.duracion.valor,
                1,
                None,
                "duracion invalida",
                "duracion",
            ),
            _ValidDuracionunidad(self.entrenamiento.duracion.unidad),
            ValidInteger(
                self.entrenamiento.duracion.series,
                1,
                None,
                "cantidad de series invalida",
                "series",
            ),
        ]

        super().__init__(message, rules, "entrenamiento")


class _ValidCategoria(BusinessRule):
    categoria: str

    def __init__(self, categoria, message="La categoria no es una opcion valida"):
        super().__init__(message, "categoria")
        self.categoria = categoria

    def is_valid(self) -> bool:
        return self.categoria in PLAN_CATEGORIA.list()


class _ValidExigencia(BusinessRule):
    exigencia: str

    def __init__(
        self, exigencia, message="El nivel de exigencia no es una opcion valida"
    ):
        super().__init__(message, "exigencia")
        self.exigencia = exigencia

    def is_valid(self) -> bool:
        return self.exigencia in EXIGENCIA.list()


class _ValidDeporte(BusinessRule):
    deporte: str

    def __init__(self, deporte, message="El deporte no es una opcion valida"):
        super().__init__(message, "deporte")
        self.deporte = deporte

    def is_valid(self) -> bool:
        return self.deporte in DEPORTE.list()


class ValidObjetivo(CompoundBusinessRule):
    objetivo: ObjetivoEntrenamiento

    def __init__(self, objetivo: ObjetivoEntrenamiento, message="objetivo invalido"):
        self.objetivo: ObjetivoEntrenamiento = objetivo

        rules = [
            _ValidExigencia(self.objetivo.exigencia),
            _ValidDeporte(self.objetivo.deporte),
        ]

        super().__init__(message, rules, "plan")


class ValidPlanEntrenamiento(CompoundBusinessRule):
    plan: PlanEntrenamiento

    def __init__(self, plan: PlanEntrenamiento, message="plan invalido"):
        self.plan: PlanEntrenamiento = plan

        rules = [
            ValidString(self.plan.nombre, 2, 120, "nombre invalido", "nombre"),
            ValidString(
                self.plan.descripcion, 2, 400, "descripcion invalida", "descripcion"
            ),
            _ValidCategoria(self.plan.categoria),
            ValidObjetivo(self.plan.objetivo),
        ]

        super().__init__(message, rules, "plan")


class ValidUsuarioPlan(CompoundBusinessRule):
    usuario: UsuarioPlan

    def __init__(self, usuario: UsuarioPlan, message="usuario invalido"):
        self.usuario: UsuarioPlan = usuario

        rules = [
            ValidString(
                self.usuario.tipo_identificacion,
                2,
                None,
                "tipo identificacion invalido",
                "tipo_identificacion",
            ),
            ValidString(
                self.usuario.identificacion,
                2,
                None,
                "identificacion invalida",
                "identificacion",
            ),
        ]

        super().__init__(message, rules, "usuario_plan")
