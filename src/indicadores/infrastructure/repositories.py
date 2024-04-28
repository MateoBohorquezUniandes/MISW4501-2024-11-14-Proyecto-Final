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

    def get(self, sesion_id:str) -> list[Indicador]:
        indicadores_dto = (
            db.session.query(IndicadorDTO)
            .filter_by(idSesion = sesion_id)
        )
        return [ self.indice_factory.create(dto, IndicadorMapper())
        for dto in indicadores_dto
        ]

    def get_last_formula_id(self, formula_id:str, tipo_identificacion:str, identificacion:str) -> Indicador:
        try:
            indicador_dto = (
                db.session.query(IndicadorDTO)
                .filter_by(tipo_identificacion=tipo_identificacion)
                .filter_by(identificacion=identificacion)
                .filter_by(idFormula=formula_id)
                .order_by(IndicadorDTO.created_at.desc())
                .one()
            )
            return self.indice_factory.create(indicador_dto, IndicadorMapper())
        except Exception:
            return Indicador(
                valor= float(0)
            )

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

    def get_all(self,tipo_identificacion:str, identificacion:str) -> list[Formula]:
        formulas_dto = (
            db.session.query(FormulaDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion).all())
        return [
            self.indice_factory.create(dto, FormulaMapper())
            for dto in formulas_dto
        ]
    
    def get(self,formula_id:str) -> Formula:
        formula_dto = (
            db.session.query(FormulaDTO)
            .filter_by(id = formula_id)
            .one()
        )
        return self.indice_factory.create(formula_dto, FormulaMapper())

    def append(self, formula: Formula):
        formula_dto: FormulaDTO = self.indice_factory.create(
            formula, FormulaMapper()
        )
        db.session.add(formula_dto)

    def delete(self, id: str):
        pass

    def update(self, indice: Indicador):
        pass