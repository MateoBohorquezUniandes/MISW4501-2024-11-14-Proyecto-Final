from seedwork.domain.rules import CompoundBusinessRule, ValidString
from autenticador.domain.value_objects import Identidad


class ValidTokenIdentity(CompoundBusinessRule):
    identity: Identidad

    def __init__(self, identity: Identidad, message="solicitud de token invalido"):
        self.identity = identity

        rules = [
            ValidString(
                self.identity.tipo,
                1,
                None,
                "El tipo de la identidad debe existir",
                "tipo",
            ),
            ValidString(
                self.identity.valor,
                1,
                None,
                "El valor de la identidad debe existir",
                "valor",
            ),
            ValidString(
                self.identity.valor,
                1,
                None,
                "El rol de la identidad debe existir",
                "rol",
            ),
        ]

        super().__init__(message, rules, "validation.credenciales")
