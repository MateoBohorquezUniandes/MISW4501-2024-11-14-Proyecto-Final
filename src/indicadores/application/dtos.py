from dataclasses import dataclass, field

from seedwork.application.dtos import DTO

@dataclass(frozen=True)
class ParametroDTO(DTO):
    id: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    simbolo: str = field(default_factory=str)
    funcion: str = field(default_factory=str)

@dataclass(frozen=True)
class FormulaDTO(DTO):
    id: str = field(default_factory=str)

    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)

    nombre: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    formula: str = field(default_factory=str)

    parametros: list[ParametroDTO] = field(default_factory=list[ParametroDTO])

@dataclass(frozen=True)
class ValorParametroDTO(DTO):
    nombre: str = field(default_factory=str)
    valores: list[int] = field(default_factory=list[int])

@dataclass(frozen=True)
class IndicadorDTO(DTO):
    idSesion: str = field(default_factory=str)
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
    parametros: list[ValorParametroDTO] = field(default_factory=list[ValorParametroDTO])