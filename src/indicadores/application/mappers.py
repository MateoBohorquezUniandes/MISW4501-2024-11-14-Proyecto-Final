import uuid
from uuid import UUID
from seedwork.application.dtos import Mapper as ApplicationMapper
from seedwork.domain.entities import Entity
from seedwork.domain.repositories import Mapper as DomainMapper
from indicadores.application.dtos import FormulaDTO, ParametroDTO, IndicadorDTO, ValorParametroDTO
from indicadores.domain.entities import Indicador, Formula
from indicadores.domain.value_objects import Parametro

TIPO_GLOBAL = "global"
IDENTIFICACION_GLOBAL = "global"

# #####################################################################################
# Application Mappers
# #####################################################################################

class FormulaDTODictMapper(ApplicationMapper):
    def _external_to_parametros_dto(self, external:dict) -> list[ParametroDTO]:
        parametros : list[ParametroDTO] = list()
        for parametro in external.keys():
            parametro_int = external.get(parametro)
            parametros.append(
                ParametroDTO(
                    id=parametro_int.get("id",""),
                    nombre=str(parametro),
                    simbolo=parametro_int.get("simbolo"),
                    funcion=parametro_int.get("funcion"))
            )
        return parametros

    def external_to_dto(self, external:dict) -> FormulaDTO:
        if(external.get('global') != None and external.get('global') == 1):
            tipo_identificacion = TIPO_GLOBAL
            identificacion = IDENTIFICACION_GLOBAL
        else:
            tipo_identificacion = external.get("tipo_identificacion")
            identificacion = external.get("identificacion")
        parametros = self._external_to_parametros_dto(external.get("parametros"))
        return FormulaDTO(
            id=external.get("id", ""),
            tipo_identificacion=tipo_identificacion,
            identificacion=identificacion,
            nombre=external.get("nombre"),
            descripcion=external.get("descripcion"),
            formula=external.get("formula"),
            parametros=parametros,
        )

    def dto_to_external(self, dto: FormulaDTO) -> dict:
        return dto.__dict__
    
class IndicadoresDTODictMapper(ApplicationMapper):
    def _external_to_valores_dto(self, external:dict) -> list[ValorParametroDTO]:
        parametros_valor : list[ValorParametroDTO] = list()
        for parametro in external.keys():
            parametro_int = external.get(parametro)
            parametros_valor.append(
                ValorParametroDTO(
                    nombre=str(parametro),
                    simbolo=parametro_int
                )
            )
        return parametros_valor

    def external_to_dto(self, external:dict) -> IndicadorDTO:
        parametros = self._external_to_valores_dto(external.get("parametros"))
        return IndicadorDTO(
            idSesion=external.get("id"),
            tipo_identificacion=external.get("tipo_identificacion"),
            identificacion=external.get("identificacion"),
            parametros=parametros,
        )

    def dto_to_external(self, dto: FormulaDTO) -> dict:
        return dto.__dict__

# #####################################################################################
# Domain Mappers
# #####################################################################################

class FormulaDTOEntityMapper(DomainMapper):

    def type(self) -> type:
        return Formula
    
    def _dto_to_parametros(self, entity: list[ParametroDTO]) -> list[Parametro]: 
        parametros: list[Parametro] = list()
        for parametro in entity:
            parametros.append(Parametro(str(uuid.uuid4()),parametro.nombre,parametro.simbolo, parametro.funcion))
        return parametros
    
    def dto_to_entity(self, dto: FormulaDTO) -> Formula:
        parametros = self._dto_to_parametros(dto.parametros)
        args = [UUID(dto.id)] if dto.id else []
        return Formula(
            *args,
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            formula=dto.formula,
            parametros=parametros
        )
    def _parametro_to_dto(self, entity:Parametro) -> ParametroDTO:
        return ParametroDTO(entity.id, entity.nombre, entity.simbolo, entity.funcion)

    def entity_to_dto(self, entity: Formula) -> FormulaDTO:
        parametros_dto: list[ParametroDTO] = list()
        for parametro in entity.parametros:
            parametros_dto.append(self._parametro_to_dto(parametro)) 
        return FormulaDTO(
            entity.id,
            entity.tipo_identificacion,
            entity.identificacion,
            entity.nombre,
            entity.descripcion,
            entity.formula,
            parametros_dto
        )
    
class IndicadorDTOEntityMapper(DomainMapper):

    def type(self) -> type:
        return Indicador
    
    def entity_to_dto():
        pass

    def dto_to_entity():
        pass