from indicadores.domain.factories import IndicadorFactory, CalculatorFactory
from indicadores.infrastructure.factories import RepositoryFactory
from seedwork.application.commands import CommandHandler


class IndicadorCommandBaseHandler(CommandHandler):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._indices_factory: IndicadorFactory = IndicadorFactory()
        self._calculator_factory: CalculatorFactory = CalculatorFactory()

    @property
    def repository_factory(self):
        return self._repository_factory

    @property
    def indices_factory(self):
        return self._indices_factory
    
    @property
    def calculator_factory(self):
        return self._calculator_factory