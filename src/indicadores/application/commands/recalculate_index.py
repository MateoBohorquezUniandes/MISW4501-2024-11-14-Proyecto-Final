import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from seedwork.application.commands import Command, CommandResult, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError
from indicadores.application.commands.base import IndicadorCommandBaseHandler
from indicadores.application.dtos import FormulaDTO, IndicadorDTO
from indicadores.application.exceptions import BadRequestError, UnprocessableEntityError
from indicadores.application.mappers import IndicadorDTOEntityMapper
from indicadores.domain.entities import Formula, Indicador
from indicadores.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory
from indicadores.application.calculator import FormulaCalculator

TIPO_GLOBAL = "global"
IDENTIFICACION_GLOBAL = "global"

@dataclass
class CalculateIndicador(Command):
    indicador_dto: IndicadorDTO = field(default_factory=IndicadorDTO)

class CalculateIndicadorHandler(IndicadorCommandBaseHandler):


    def handle(self, command: CalculateIndicador) -> CommandResult:
        uowf = None
        try:
            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()
            repositorio_f = self.repository_factory.create(Formula)
            repositorio = self.repository_factory.create(Indicador)
            calculator = FormulaCalculator()
            mapper = IndicadorDTOEntityMapper()

            indicadores_calculados: list[Indicador] = list()
            formulas_usuario: list[Formula] = repositorio_f.get(command.indicador_dto.tipo_identificacion, command.indicador_dto.identificacion)
            formulas_globales: list[Formula] = repositorio_f.get(TIPO_GLOBAL, IDENTIFICACION_GLOBAL)
            formulas_usuario.extend(formulas_globales)
            
            for formula in formulas_usuario: 
                indicador: Indicador = calculator.calculate(command.indicador_dto.parametros, formula ,command.indicador_dto.idSesion)
                indicadores_calculados.append(indicador)
                UnitOfWorkPort.register_batch(uowf, repositorio.append, indicador)

            UnitOfWorkPort.commit(uowf)
            resultados_dto = [self.indices_factory.create(e, mapper) for e in indicadores_calculados]
            return CommandResult(result=resultados_dto)
        #except BusinessRuleException as bre:
        #    traceback.print_exc()
        #    raise UnprocessableEntityError(str(bre), bre.code)
        #except IntegrityError:
        #    traceback.print_exc()
        #    raise BadRequestError(code="indices.create.integrity")
        except Exception as e:
            traceback.print_exc()
            if uowf:
                UnitOfWorkPort.rollback(uowf)
            raise APIError(message=str(e), code="indices.error.internal")

@execute_command.register(CalculateIndicador)
def command_crear_indice(command: CalculateIndicador) -> CommandResult:
    return CalculateIndicadorHandler().handle(command)        