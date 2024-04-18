from seedwork.domain.rules import CompoundBusinessRule, ValidString
from sesiones.domain.entities import SesionDeportiva
from sesiones.domain.value_objects import Objetivo


class ValidObjetivo(CompoundBusinessRule):
    objetivo = Objetivo

    def __init__(self, objetivo: Objetivo, message="sesion invalido"):
        self.objetivo: Objetivo = objetivo

        rules = [
            ValidString(
                self.objetivo.exigencia,
                2,
                50,
                "exigencia invalida",
                "exigencia",
            ),
            ValidString(
                self.objetivo.deporte,
                2,
                50,
                "deporte invalido",
                "deporte",
            ),
        ]

        super().__init__(message, rules, "objetivo")


class ValidSesionDeportiva(CompoundBusinessRule):
    sesion: SesionDeportiva

    def __init__(self, sesion: SesionDeportiva, message="sesion invalido"):
        self.sesion: SesionDeportiva = sesion

        rules = [
            ValidString(
                self.sesion.tipo_identificacion,
                2,
                10,
                "tipo identificacion invalido",
                "tipo_identificacion",
            ),
            ValidString(
                self.sesion.identificacion,
                2,
                20,
                "identificacion invalida",
                "identificacion",
            ),
            ValidObjetivo(self.sesion.objetivo),
        ]

        super().__init__(message, rules, "sesion")
