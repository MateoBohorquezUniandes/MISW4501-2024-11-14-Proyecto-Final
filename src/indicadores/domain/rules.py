import numexpr

from seedwork.domain.rules import CompoundBusinessRule, BusinessRule, ValidString, ValidFloat
from indicadores.domain.entities import Formula, Indicador
from indicadores.domain.value_objects import Parametro

class _ValidFormula(BusinessRule):
    formula:str
    def __init__(self, formula:str, parametros:list[Parametro], message="formula inejecutable"):
        super().__init__(message, "unidad")
        self.formula = formula
        self.parametros = parametros
    
    def is_valid(self) -> bool:
        compilada = compile(self.formula,'formular','exec')
        if(len(compilada.co_names) != len(self.parametros)):
            return False
        formula = self.formula
        for variable in compilada.co_names:
            formula = formula.replace(variable,str(1))
        try:
            numexpr.evaluate(formula)
            return True
        except:
            return False

class ValidParametro(CompoundBusinessRule):
    parametro: Parametro

    def __init__(self, parametro:Parametro, message="parametro invalido"):
        self.parametro: Parametro = parametro
        rules = [
            ValidString(
                self.parametro.nombre,
                3,
                20,
                "nombre de parametro invalido:" + str(self.parametro.simbolo),
                "nombre"),
            ValidString(
                self.parametro.simbolo,
                1,
                1,
                "simbolo de parametro invalido:" + str(self.parametro.simbolo),
                "simbolo"),
            ValidString(
                self.parametro.funcion,
                3,
                3,
                "funcion de parametro invalido:" + str(self.parametro.simbolo)),
        ]

class ValidFormula(CompoundBusinessRule):
    def __init__(self, formula: Formula, message="formula invalida"):
        self.formula: Formula = formula

        rules = [
            ValidString(
                self.formula.tipo_identificacion,
                2,
                10,
                "tipo identificacion invalido",
                "tipo_identificacion",
            ),
            ValidString(
                self.formula.identificacion,
                2,
                20,
                "identificacion invalida",
                "identificacion",
            ),
            ValidString(
                self.formula.nombre,
                2,
                20,
                "nombre invalido",
                "nombre",
            ),
            ValidString(
                self.formula.descripcion,
                2,
                100,
                "descripcion invalida",
                "descripcion",
            ),
            ValidString(
                self.formula.formula,
                1,
                100,
                "formula invalida",
                "formula",
            ),
            _ValidFormula(self.formula.formula, self.formula.parametros),
            #ValidParametro(e in self.formula.parametros)
            #necesito que Santi me explique esta parte

        ]
        super().__init__(message, rules, "formula")

class ValidIndicador(CompoundBusinessRule):
    def __init__(self, indicador: Indicador, message="indicador invalido"):
        self.indicador: Indicador = indicador

        rules = [
            ValidString(
                self.indicador.idSesion,
                36,
                36,
                "idSesion invalido",
                "idSesion"
            ),
            ValidString(
                self.indicador.idFormula,
                36,
                36,
                "idFormula invalido",
                "idFormula"
            ),
            ValidString(
                self.indicador.tipo_identificacion,
                2,
                10,
                "tipo identificacion invalido",
                "tipo_identificacion",
            ),
            ValidString(
                self.indicador.identificacion,
                2,
                20,
                "identificacion invalida",
                "identificacion",
            ),
        ]

        super().__init__(message, rules, "indicador")