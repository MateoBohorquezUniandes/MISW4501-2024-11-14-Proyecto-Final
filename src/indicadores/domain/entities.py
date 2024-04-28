from dataclasses import dataclass, field
from datetime import datetime
import uuid

from seedwork.domain.entities import RootAggregation
import indicadores.domain.value_objects as vo


@dataclass
class Indicador(RootAggregation):
    idSesion: str = field(default_factory=str)
    idFormula : str = field(default_factory=str)
    nombreFormula: str = field(default_factory=str)
    valor: float = field(default_factory=float)
    varianza: float = field(default_factory=float)
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)

@dataclass
class Formula(RootAggregation):
    tipo_identificacion: str = field(default_factory=str)
    identificacion: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    formula: str = field(default_factory=str)

    parametros: list[vo.Parametro] = field(default_factory=list[vo.Parametro])