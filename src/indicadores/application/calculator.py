import uuid
import numexpr
import numpy as np

from indicadores.application.exceptions import UnprocessableEntityError

from indicadores.application.dtos import ValorParametroDTO
from indicadores.domain.entities import Formula, Indicador
class FormulaCalculator():

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
                        raise UnprocessableEntityError()

                else:
                    continue
        return formula_resultante

    def calculate(self, valores: list[ValorParametroDTO], formula: Formula, sesionId:str, last_indicador:Indicador, tipo_identificacion:str, identificacion:str) -> Indicador:
        formula_resultante = self.simplify_values(valores, formula)
        resultado = numexpr.evaluate(formula_resultante)
        resultado = float(str(np.round(resultado, 2)))
        varianza = abs(resultado - last_indicador.valor)
        return Indicador(
            _id = uuid.uuid4(),
            idSesion = sesionId,
            idFormula = str(formula.id),
            nombreFormula=str(formula.nombre),
            valor = resultado,
            varianza = varianza,
            tipo_identificacion= str(tipo_identificacion),
            identificacion = str(identificacion)
        )
    
    def create_parametros(self, valores: list[ValorParametroDTO], formula: Formula, sesionId:str, last_indicador:Indicador, tipo_identificacion:str, identificacion:str) -> dict:
        diccionario = dict()
        diccionario["valores"] = valores
        diccionario["formula"] = formula
        diccionario["sesionId"] = sesionId
        diccionario["last_indicador"] = last_indicador
        diccionario["tipo_identificacion"] = tipo_identificacion
        diccionario["identificacion"] = identificacion
        return diccionario