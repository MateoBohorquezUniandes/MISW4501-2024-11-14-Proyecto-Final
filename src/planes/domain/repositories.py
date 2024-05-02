from abc import ABC

from seedwork.domain.repositories import Repository


class PlanEntrenamientoRepository(Repository, ABC): ...


class EntrenamientoRepository(Repository, ABC): ...


class UsuarioPlanRepository(Repository, ABC): ...


class RutinaAlimentacionRepository(Repository, ABC): ...


class GrupoAlimenticioRepository(Repository, ABC): ...
