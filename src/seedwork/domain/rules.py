from abc import ABC, abstractmethod
import datetime

from seedwork.domain.value_objects import ExtendedEnum


class BusinessRule(ABC):

    __message: str = "Invalid business rule"
    __code: str

    def __init__(self, message, code="business_rule"):
        self.__message = message
        self.__code = code

    def error(self) -> str:
        return self.__message

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, code):
        self.__code = code

    @abstractmethod
    def is_valid(self) -> bool: ...

    def __str__(self):
        return f"{self.__class__.__name__} - {self.__message}"


class CompoundBusinessRule(BusinessRule):
    __cause: str
    __rules: list[BusinessRule]

    def __init__(self, message, rules, code="rule.compound"):
        super(CompoundBusinessRule, self).__init__(message, code)
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
                self.code = f"{self.code}.{regla.code}"
                return False
        return True

    def __str__(self):
        return f"{self.__class__.__name__} > {self.__cause}"


class ImmutableEntityIdRule(BusinessRule):

    entity: object

    def __init__(self, entity, message="Entity identifier must be inmutable"):
        super().__init__(message, "entity.mutability")
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

    def __init__(self, valor, min, max, message, code="valid_string"):
        super().__init__(message, code)
        self.valor = valor
        self.min = min
        self.max = max

    def is_valid(self) -> bool:
        min_valid = len(self.valor) >= self.min if self.min else True
        max_valid = len(self.valor) <= self.max if self.max else True
        return min_valid and max_valid


class ValidFloat(BusinessRule):
    valor: float
    min: float
    max: float

    def __init__(self, valor, min, max, message, code="valid_float"):
        super().__init__(message, code)
        self.valor = valor
        self.min = min
        self.max = max

    def is_valid(self) -> bool:
        min_valid = self.valor >= self.min if self.min else True
        max_valid = self.valor <= self.max if self.max else True
        return min_valid and max_valid


class ValidInteger(BusinessRule):
    valor: float
    min: float
    max: float

    def __init__(self, valor, min, max, message, code="valid_integer"):
        super().__init__(message, code)
        self.valor = valor
        self.min = min
        self.max = max

    def is_valid(self) -> bool:
        min_valid = self.valor >= self.min if self.min else True
        max_valid = self.valor <= self.max if self.max else True
        return min_valid and max_valid


class ValidStrDate(BusinessRule):
    date: str

    def __init__(self, date, message, code="valid_Str_date"):
        super().__init__(message, code)
        self.date = date

    def is_valid(self) -> bool:
        try:
            res = bool(datetime.date.fromisoformat(self.date))
        except ValueError:
            res = False

        return res


class ValidExtendedEnum(BusinessRule):
    value: any
    enumeration: type[ExtendedEnum]

    def __init__(
        self,
        value: any,
        enumeration: type[ExtendedEnum],
        message,
        code="valid_ext_enum",
        soft_check=False,
    ):
        super().__init__(message, code)
        self.value = value
        self.enumeration = enumeration
        self.soft_check = soft_check

    def is_valid(self) -> bool:
        return (
            self.value in self.enumeration.list()
            if not self.soft_check
            else True
        )
