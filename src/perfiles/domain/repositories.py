from abc import ABC

from seedwork.domain.repositories import Repository


class PerfilDemograficoRepository(Repository, ABC): ...


class PerfilDeportivoRepository(Repository, ABC): ...


class PerfilAlimenticioRepository(Repository, ABC): ...


class HabitoDeportivoRepository(Repository, ABC): ...


class MolestiaRepository(Repository, ABC): ...
