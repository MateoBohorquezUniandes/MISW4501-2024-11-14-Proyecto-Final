import traceback
from dataclasses import dataclass, field

from sqlalchemy.exc import IntegrityError

from seedwork.application.commands import Command, CommandResult, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError
from indicadores.application.commands.base import IndicadorCommandBaseHandler
from indicadores.application.dtos import FormulaDTO
from indicadores.application.exceptions import BadRequestError, UnprocessableEntityError
from indicadores.application.mappers import FormulaDTOEntityMapper
from indicadores.domain.entities import Formula
from indicadores.infrastructure.uwo import UnitOfWorkASQLAlchemyFactory

@dataclass
class CreateFormula(Command):
    formula_dto: FormulaDTO = field(default_factory=FormulaDTO)

class CreateFormulaHandler(IndicadorCommandBaseHandler):
    def handle(self, command: CreateFormula) -> CommandResult:
        uowf = None
        try:
            uowf: UnitOfWorkASQLAlchemyFactory = UnitOfWorkASQLAlchemyFactory()
            mapper = FormulaDTOEntityMapper()
            formula: Formula = self.indices_factory.create(
                command.formula_dto, mapper
            )
            #repositorio_f = self.repository_factory.create(Formula)
            #repositorio = self.repository_factory.create(indice)
            #repositorio_f.get all formulas(tipoidentificacion, identificacion) -> Repositories Formulas
            #for formula in formulas: 
            #    indicador = formula.calculate(parametros, sesionId)
            #    UnitOfWorkPort.register_batch(uowf, repositorio.append, indicador)
            
            repositorio = self.repository_factory.create(formula)
            UnitOfWorkPort.register_batch(uowf, repositorio.append, formula)
            UnitOfWorkPort.commit(uowf)

            return CommandResult(self.indices_factory.create(formula, mapper))
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

@execute_command.register(CreateFormula)
def command_crear_indice(command: CreateFormula) -> CommandResult:
    return CreateFormulaHandler().handle(command)        