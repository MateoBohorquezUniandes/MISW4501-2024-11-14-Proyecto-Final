from planes.domain.entities import (
    Entrenamiento,
    GrupoAlimenticio,
    PlanEntrenamiento,
    RutinaAlimentacion,
    RutinaRecuperacion,
    UsuarioPlan,
)
from planes.domain.value_objects import (
    DEPORTE,
    DURACION_UNIDAD,
    EXIGENCIA,
    PLAN_CATEGORIA,
    PORCION_UNIDAD,
    ObjetivoEntrenamiento,
)
from seedwork.domain.rules import (
    BusinessRule,
    CompoundBusinessRule,
    ValidExtendedEnum,
    ValidFloat,
    ValidInteger,
    ValidString,
)
from seedwork.domain.value_objects import CATEGORIA_ALIMENTO, TIPO_ALIMENTACION


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
            ValidExtendedEnum(
                self.entrenamiento.duracion.unidad,
                DURACION_UNIDAD,
                "duracion invalida",
                "duracion",
            ),
            ValidInteger(
                self.entrenamiento.duracion.series,
                1,
                None,
                "cantidad de series invalida",
                "series",
            ),
        ]

        super().__init__(message, rules, "entrenamiento")


class ValidObjetivo(CompoundBusinessRule):
    objetivo: ObjetivoEntrenamiento

    def __init__(self, objetivo: ObjetivoEntrenamiento, message="objetivo invalido"):
        self.objetivo: ObjetivoEntrenamiento = objetivo

        rules = [
            ValidExtendedEnum(
                self.objetivo.exigencia, EXIGENCIA, "exigencia invalida", "exigencia"
            ),
            ValidExtendedEnum(
                self.objetivo.deporte, DEPORTE, "deporte invalido", "deporte"
            ),
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
            ValidExtendedEnum(
                self.plan.categoria, PLAN_CATEGORIA, "categoria invalida", "categoria"
            ),
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


class ValidGrupoAlimenticio(CompoundBusinessRule):
    grupo: GrupoAlimenticio

    def __init__(self, grupo: GrupoAlimenticio, message="usuario invalido"):
        self.grupo: GrupoAlimenticio = grupo

        rules = [
            ValidExtendedEnum(
                self.grupo.grupo, CATEGORIA_ALIMENTO, "grupo invalido", "grupo"
            ),
            ValidFloat(
                self.grupo.porcion,
                1,
                None,
                "porcion fuera de rango invalida",
                "porcion",
            ),
            ValidFloat(
                self.grupo.calorias,
                1,
                None,
                "calorias fuera de rango invalida",
                "calorias",
            ),
            ValidExtendedEnum(
                self.grupo.unidad, PORCION_UNIDAD, "unidad invalida", "unidad"
            ),
        ]

        super().__init__(message, rules, "grupo_alimenticio")


class ValidRutinaAlimentacion(CompoundBusinessRule):
    rutina: RutinaAlimentacion

    def __init__(self, rutina: RutinaAlimentacion, message="usuario invalido"):
        self.rutina: RutinaAlimentacion = rutina

        rules = [
            ValidString(self.rutina.nombre, 2, 120, "nombre invalido", "nombre"),
            ValidString(
                self.rutina.descripcion, 2, 120, "descripcion invalida", "descripcion"
            ),
            ValidString(self.rutina.imagen, 2, 400, "imagen invalida", "imagen"),
            ValidExtendedEnum(
                self.rutina.deporte, DEPORTE, "deporte invalido", "deporte"
            ),
            ValidExtendedEnum(
                self.rutina.tipo_alimentacion,
                TIPO_ALIMENTACION,
                "tipo invalido",
                "tipo",
            ),
        ]
        rules.extend(
            [ValidGrupoAlimenticio(g) for g in self.rutina.grupos_alimenticios]
        )

        super().__init__(message, rules, "rutina.alimentacion")


class ValidRutinaRecuperacion(CompoundBusinessRule):
    rutina: RutinaRecuperacion

    def __init__(self, rutina: RutinaRecuperacion, message="usuario invalido"):
        self.rutina: RutinaRecuperacion = rutina

        rules = [
            ValidString(self.rutina.nombre, 2, 120, "nombre invalido", "nombre"),
            ValidString(
                self.rutina.descripcion, 2, 120, "descripcion invalida", "descripcion"
            ),
            ValidString(self.rutina.imagen, 2, 400, "imagen invalida", "imagen"),
            ValidExtendedEnum(
                self.rutina.deporte, DEPORTE, "deporte invalido", "deporte"
            ),
            ValidInteger(
                self.rutina.frecuencia.valor,
                1,
                None,
                "duracion invalida",
                "duracion",
            ),
            ValidExtendedEnum(
                self.rutina.frecuencia.unidad,
                DURACION_UNIDAD,
                "duracion invalida",
                "duracion",
            ),
        ]

        super().__init__(message, rules, "rutina.recuperacion")
