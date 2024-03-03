from .rules import BusinessRule


class DomainException(Exception): ...


class MutableEntityIdException(DomainException):
    def __init__(self, mensaje="Identifier must be immutable"):
        self.__message = mensaje

    def __str__(self):
        return str(self.__message)


class BusinessRuleException(DomainException):
    def __init__(self, rule: BusinessRule):
        self.rule = rule

    def __str__(self):
        return str(self.rule)


class FactoryException(DomainException):
    def __init__(self, mensaje):
        self.__message = mensaje

    def __str__(self):
        return str(self.__message)
