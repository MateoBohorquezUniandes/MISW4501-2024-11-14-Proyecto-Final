from dataclasses import dataclass

from seedwork.domain.factories import Factory
from indicadores.domain.entities import Indicador, Formula
from indicadores.infrastructure.exceptions import InvalidRepositoryFactoryException
from indicadores.infrastructure.repositories import IndicadorRepositoryPostgreSQL, FormulaRepositoryPostgreSQL


@dataclass
class RepositoryFactory(Factory):
    def create(self, obj):
        if isinstance(obj, Indicador) or obj == Indicador:
            return IndicadorRepositoryPostgreSQL()
        elif isinstance(obj, Formula) or obj == Formula:
            return FormulaRepositoryPostgreSQL()
        else:
            raise InvalidRepositoryFactoryException()