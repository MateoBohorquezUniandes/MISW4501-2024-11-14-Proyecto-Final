from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import singledispatch


class Query(ABC): ...


@dataclass
class QueryResult:
    result: any


class QueryHandler(ABC):
    @abstractmethod
    def handle(self, query: Query) -> QueryResult:
        raise NotImplementedError()


@singledispatch
def execute_query(query) -> QueryResult:
    raise NotImplementedError(
        f"Missing query execution implementation for {type(query).__name__}"
    )
