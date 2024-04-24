from eventos.domain.entities import Evento
from eventos.domain.value_objects import EventoTipoEnum, EXIGENCIA

from seedwork.domain.rules import (
    BusinessRule,
    CompoundBusinessRule,
    ValidFloat,
    ValidInteger,
    ValidString,
    ValidStrDate,
)


class _ValidEventoTipo(BusinessRule):
    tipo: str

    def __init__(self, evento, message="El tipo de evento no es una opcion valida"):
        super().__init__(message, "evento")
        self.tipo = evento

    def is_valid(self) -> bool:
        return self.tipo in EventoTipoEnum.list()


class _ValidNivel(BusinessRule):
    nivel: str

    def __init__(
        self, exigencia, message="El nivel de exigencia no es una opcion valida"
    ):
        super().__init__(message, "exigencia")
        self.nivel = exigencia

    def is_valid(self) -> bool:
        return self.nivel in EXIGENCIA.list()


class ValidEvento(CompoundBusinessRule):
    evento: Evento

    def __init__(self, molestia: Evento, message="evento invalido"):
        self.evento: Evento = molestia

        rules = [
            ValidString(self.evento.lugar, 2, 2000, "lugar invalido"),
            _ValidEventoTipo(self.evento.tipo),
            ValidStrDate(self.evento.fecha, "fecha invalida"),
            _ValidNivel(self.evento.nivel),
        ]

        super().__init__(message, rules, "evento")
