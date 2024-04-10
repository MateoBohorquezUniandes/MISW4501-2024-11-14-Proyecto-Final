from abc import ABC, abstractmethod
from uuid import UUID
from .entities import Entity


class Repository(ABC):
    @abstractmethod
    def get(self, *args, **kwargs) -> Entity: ...

    @abstractmethod
    def get_all(self, *args, **kwargs) -> list[Entity]: ...

    @abstractmethod
    def append(self, entity: Entity, *args, **kwargs): ...

    @abstractmethod
    def update(self, entity: Entity, *args, **kwargs): ...

    @abstractmethod
    def delete(self, *args, **kwargs): ...


class Mapper(ABC):
    @abstractmethod
    def type(self) -> type: ...

    @abstractmethod
    def entity_to_dto(self, entity: Entity) -> any: ...

    @abstractmethod
    def dto_to_entity(self, dto: any) -> Entity: ...


class UnidirectionalMapper(ABC):
    @abstractmethod
    def type(self) -> type: ...

    @abstractmethod
    def map(self, value: any) -> any: ...
