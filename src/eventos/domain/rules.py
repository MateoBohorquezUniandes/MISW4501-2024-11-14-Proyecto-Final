from eventos.domain.entities import Evento
from eventos.domain.value_objects import EXIGENCIA
from seedwork.domain.rules import (
    CompoundBusinessRule,
    ValidExtendedEnum,
    ValidStrDate,
    ValidString,
)
from seedwork.domain.value_objects import DEPORTE


class ValidEvento(CompoundBusinessRule):
    evento: Evento

    def __init__(self, molestia: Evento, message="evento invalido"):
        self.evento: Evento = molestia

        rules = [
            ValidString(self.evento.lugar, 2, 2000, "lugar invalido"),
            ValidExtendedEnum(self.evento.tipo, DEPORTE, "tipo invalido", "tipo"),
            ValidStrDate(self.evento.fecha, "fecha invalida"),
            ValidExtendedEnum(
                self.evento.nivel, EXIGENCIA, "exigencia invalida", "exigencia"
            ),
        ]

        super().__init__(message, rules, "evento")
