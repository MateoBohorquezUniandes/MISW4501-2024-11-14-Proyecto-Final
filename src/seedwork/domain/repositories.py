from abc import ABC, abstractmethod
from uuid import UUID
from .entities import Entity


class Repository(ABC):
    @abstractmethod
    def get(self, *args) -> Entity: ...

    @abstractmethod
    def get_all(self) -> list[Entity]: ...

    @abstractmethod
    def append(self, entity: Entity): ...

    @abstractmethod
    def update(self, entity: Entity): ...

    @abstractmethod
    def delete(self, entity_id: UUID): ...


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
