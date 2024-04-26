from uuid import UUID
from indicadores.domain.entities import Indicador, Formula
from indicadores.domain.value_objects import Parametro
from indicadores.infrastructure.dtos import Indicador as IndicadorDTO
from indicadores.infrastructure.dtos import Formula as FormulaDTO
from indicadores.infrastructure.dtos import Parametro as ParametroDTO

class IndicadorMapper:
    def type(self) -> type:
        return Indicador
    
    def _parametro_to_dto(self, entity: Parametro) -> ParametroDTO:
        return ParametroDTO(nombre=entity.nombre, descripcion=entity.descripcion)
    
    def entity_to_dto(self, entity:Indicador) -> IndicadorDTO:
        parametros: list[ParametroDTO] = list()
        for parametro in entity.parametros:
            parametros.append(self._parametro_to_dto(parametro))
        indice_dto = IndicadorDTO()
        indice_dto.id = str(entity.id)
        indice_dto.nombre = entity.nombre
        indice_dto.descripcion = entity.descripcion
        indice_dto.formula = entity.formula
        indice_dto.parametros = parametros
        return indice_dto

    def dto_to_entity():
        pass

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
        