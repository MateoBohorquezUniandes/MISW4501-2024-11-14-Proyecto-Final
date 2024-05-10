from dataclasses import dataclass

from seedwork.application.dtos import Mapper
from seedwork.domain.entities import Entity
from seedwork.domain.events import DomainEvent
from seedwork.domain.factories import Factory
from indicadores.domain.entities import Indicador, Formula
from indicadores.domain.exceptions import InvalidIndicadorFactoryException
from indicadores.domain.rules import ValidFormula, ValidIndicador
from indicadores.application.calculator import FormulaCalculator
from seedwork.domain.repositories import UnidirectionalMapper


@dataclass
class _IndicadorFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None) -> Indicador:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            if isinstance(mapper, UnidirectionalMapper):
                return mapper.map(obj)
            return mapper.entity_to_dto(obj)

        indicador: Indicador = mapper.dto_to_entity(obj)
        self.validate_rule(ValidIndicador(indicador))

        return indicador
    
@dataclass
class _FormulaFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None) -> Formula:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)
        
        formula: Formula = mapper.dto_to_entity(obj)
        self.validate_rule(ValidFormula(formula))

        return formula

@dataclass
class IndicadorFactory(Factory):
    def create(self, obj: any, mapper: Mapper):
        if mapper.type() == Indicador:
            indicador_factory = _IndicadorFactory()
            return indicador_factory.create(obj, mapper)
        elif mapper.type() == Formula:
            formula_factory = _FormulaFactory()
            return formula_factory.create(obj, mapper)
        else:
            raise InvalidIndicadorFactoryException()

@dataclass
class CalculatorFactory(Factory):
    def create(self,obj: any = None, mapper: Mapper = None, params = None):
        calculator = FormulaCalculator()
        indicador: Indicador = calculator.calculate(
            params["valores"],
            params["formula"],
            params["sesionId"],
            params["last_indicador"],
            params["tipo_identificacion"],
            params["identificacion"])
        self.validate_rule(ValidIndicador(indicador))
        return indicador
        