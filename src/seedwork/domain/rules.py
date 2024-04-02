from abc import ABC, abstractmethod


class BusinessRule(ABC):

    __message: str = "Invalid business rule"

    def __init__(self, message):
        self.__message = message

    def error(self) -> str:
        return self.__message

    @abstractmethod
    def is_valid(self) -> bool: ...

    def __str__(self):
        return f"{self.__class__.__name__} - {self.__message}"


class CompoundBusinessRule(BusinessRule):
    __cause: str
    __rules: list[BusinessRule]

    def __init__(self, message, rules):
        super(CompoundBusinessRule, self).__init__(message)
        self.__rules = rules

    @property
    def cause(self):
        return self.__cause

    @cause.setter
    def cause(self, cause):
        self.__cause = cause

    def is_valid(self) -> bool:
        for regla in self.__rules:
            if not regla.is_valid():
                self.cause = str(regla)
                return False
        return True

    def __str__(self):
        return f"{self.__class__.__name__} > {self.__cause}"


class ImmutableEntityIdRule(BusinessRule):

    entity: object

    def __init__(self, entity, message="Entity identifier must be inmutable"):
        super().__init__(message)
        self.entity = entity

    def is_valid(self) -> bool:
        try:
            if self.entity._id:
                return False
        except AttributeError as error:
            return True


class ValidString(BusinessRule):
    valor: str
    min: int
    max: int

    def __init__(self, valor, min, max, message):
        super().__init__(message)
        self.valor = valor
        self.min = min
        self.max = max

    def is_valid(self) -> bool:
        min_valid = len(self.valor) >= self.min if self.min else True
        max_valid = len(self.valor) <= self.max if self.max else True
        return min_valid and max_valid
