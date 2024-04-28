from uuid import UUID
from indicadores.domain.entities import Indicador, Formula
from indicadores.domain.value_objects import Parametro
from indicadores.infrastructure.dtos import Indicador as IndicadorDTO
from indicadores.infrastructure.dtos import Formula as FormulaDTO
from indicadores.infrastructure.dtos import Parametro as ParametroDTO

class IndicadorMapper:
    def type(self) -> type:
        return Indicador
    
    def entity_to_dto(self, entity:Indicador) -> IndicadorDTO:
        indicador_dto = IndicadorDTO()
        indicador_dto.idSesion = entity.idSesion
        indicador_dto.idFormula = entity.idFormula
        indicador_dto.valor = entity.valor
        indicador_dto.varianza = entity.varianza
        indicador_dto.identificacion = entity.identificacion
        indicador_dto.tipo_identificacion = entity.tipo_identificacion
        return indicador_dto

    def dto_to_entity(self, dto:IndicadorDTO) -> Indicador:
        return Indicador(
            idSesion=dto.idSesion,
            created_at=dto.created_at,
            idFormula=dto.idFormula,
            valor=dto.valor,
            varianza=dto.varianza,
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion
        )

class FormulaMapper:
    def type(self) -> type:
        return Formula
    
    def _parametro_to_dto(self, entity: Parametro, id_formula:str) -> ParametroDTO:
        return ParametroDTO(id=entity.id, nombre=entity.nombre, simbolo=entity.simbolo, funcion=entity.funcion, id_formula=id_formula)
    
    def entity_to_dto(self, entity:Formula) -> FormulaDTO:
        parametros: list[ParametroDTO] = list()
        for parametro in entity.parametros:
            parametros.append(self._parametro_to_dto(parametro, str(entity.id)))
        formula_dto = FormulaDTO()
        formula_dto.id = str(entity.id)
        formula_dto.tipo_identificacion = entity.tipo_identificacion
        formula_dto.identificacion = entity.identificacion
        formula_dto.nombre = entity.nombre
        formula_dto.descripcion = entity.descripcion
        formula_dto.formula = entity.formula
        formula_dto.parametros = parametros
        return formula_dto
    
    def _dto_to_parametro(self, dto: ParametroDTO):
        return Parametro(dto.id,dto.nombre,dto.simbolo,dto.funcion)

    def dto_to_entity(self, dto:FormulaDTO) -> Formula:
        parametros: list[Parametro] = list()
        for parametro in dto.parametros:
            parametros.append(self._dto_to_parametro(parametro))
        return Formula(
            _id=UUID(dto.id),
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            formula=dto.formula,
            parametros=parametros
        )
        