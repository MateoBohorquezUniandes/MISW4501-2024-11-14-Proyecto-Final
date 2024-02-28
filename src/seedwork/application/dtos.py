from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class DTO: ...


class Mapper(ABC):
    @abstractmethod
    def external_to_dto(self, external: any) -> DTO: ...

    @abstractmethod
    def dto_to_external(self, dto: DTO) -> any: ...
