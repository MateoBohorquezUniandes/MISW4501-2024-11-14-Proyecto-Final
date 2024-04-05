from .rules import BusinessRule


class DomainException(Exception):
    def __init__(self, message, code=None):
        self.__message = message
        self.__code = code

    def __str__(self):
        return str(self.__message)

    @property
    def code(self):
        return self.__code


class MutableEntityIdException(DomainException):
    def __init__(self, message="Identifier must be immutable"):
        super().__init__(message, "mutability.entity.id")


class BusinessRuleException(DomainException):
    def __init__(self, rule: BusinessRule):
        self.rule = rule
        super().__init__(str(rule), rule.code)


class FactoryException(DomainException):
    def __init__(self, message="invalid type for factory", code=None):
        super().__init__(message, code)
