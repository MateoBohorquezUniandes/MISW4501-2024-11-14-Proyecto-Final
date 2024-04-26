import uuid
import numexpr
import numpy as np

from indicadores.application.dtos import ValorParametroDTO
from indicadores.domain.entities import Formula, Indicador
class FormulaCalculator():
    
    def replace_params(self, formula: str, parametros: dict):
        pass

    def simplify_values(self,valores: list[ValorParametroDTO], formula: Formula) -> str:
        formula_resultante:str = formula.formula 
        for valor in valores:
            for param in formula.parametros:
                if(param.nombre == valor.nombre):
                    if(param.funcion == "min"):
                        formula_resultante = formula_resultante.replace(param.simbolo,str(min(valor.valores)))
                    elif(param.funcion == "avg"):
                        formula_resultante = formula_resultante.replace(param.simbolo,str((sum(valor.valores)/len(valor.valores))))
                    elif(param.funcion == "max"):
                        formula_resultante = formula_resultante.replace(param.simbolo,str(max(valor.valores)))
                    else:
                        pass # arrojar execption

                else:
                    continue
        return formula_resultante


    def compile(self, parametros, formula):
        pass

    def calculate(self, valores: list[ValorParametroDTO], formula: Formula, sesionId:str) -> Indicador:
        formula_resultante = self.simplify_values(valores, formula)
        resultado = numexpr.evaluate(formula_resultante)
        return Indicador(
            _id = uuid.uuid4(),
            idSesion = sesionId,
            idFormula = str(formula.id),
            nombreFormula=str(formula.nombre),
            valor = str(np.round(resultado, 2)),
            varianza = str(0)
        )