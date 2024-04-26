from typing import Union
from indicadores.domain.entities import Indicador, Formula
from indicadores.domain.factories import IndicadorFactory
from indicadores.domain.repositories import IndicadorRepository
from indicadores.infrastructure.dtos import Indicador as IndicadorDTO
from indicadores.infrastructure.dtos import Formula as FormulaDTO
from indicadores.infrastructure.db import db
from indicadores.infrastructure.mappers import IndicadorMapper, FormulaMapper


class IndicadorRepositoryPostgreSQL(IndicadorRepository):
    def __init__(self):
        self._indice_factory: IndicadorFactory = IndicadorFactory()

    @property
    def indice_factory(self):
        return self._indice_factory

    def get_all():
        pass

    def get():
        pass

    def append(self, indicador: Indicador):
        indicador_dto: IndicadorDTO = self.indice_factory.create(
            indicador, IndicadorMapper()
        )
        db.session.add(indicador_dto)

    def delete(self, id: str):
        pass

    def update(self, indice: Indicador):
        pass

class FormulaRepositoryPostgreSQL(IndicadorRepository): 
    def __init__(self):
        self._indice_factory: IndicadorFactory = IndicadorFactory()

    @property
    def indice_factory(self):
        return self._indice_factory

    def get_all():
        pass

    def get(self,tipo_identificacion:str, identificacion:str) -> list[Formula]:
        formulas_dto = (
            db.session.query(FormulaDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion))
        return [
            self.indice_factory.create(dto, FormulaMapper())
            for dto in formulas_dto
        ]

    def append(self, formula: Formula):
        formula_dto: FormulaDTO = self.indice_factory.create(
            formula, FormulaMapper()
        )
        db.session.add(formula_dto)

    def delete(self, id: str):
        pass

    def update(self, indice: Indicador):
        pass