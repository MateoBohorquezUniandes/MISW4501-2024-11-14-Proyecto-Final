from abc import ABC

from seedwork.domain.repositories import Repository


class EventoRepository(Repository, ABC): ...


class EventoAsociadoRepository(Repository, ABC): ...
