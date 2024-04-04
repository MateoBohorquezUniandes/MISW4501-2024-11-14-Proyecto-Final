from abc import ABC

from seedwork.domain.repositories import Repository


class DeportistaRepository(Repository, ABC): ...


class OrganizadorRepository(Repository, ABC): ...


class SocioRepository(Repository, ABC): ...
