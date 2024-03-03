from .exceptions import BusinessRuleException
from .rules import BusinessRule


class RuleValidationMixin:
    def validate_rule(self, regla: BusinessRule):
        if not regla.es_valido():
            raise BusinessRuleException(regla)
