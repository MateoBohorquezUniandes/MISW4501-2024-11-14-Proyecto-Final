from productos.domain.factories import ProductoFactoy
from productos.infrastructure.factories import RepositoryFactory

from seedwork.application.commands import CommandHandler


class ProductoCommandBaseHandler(CommandHandler):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._productos_factory: ProductoFactoy = ProductoFactoy()

    @property
    def repository_factory(self):
        return self._repository_factory

    @property
    def productos_factory(self):
        return self._productos_factory
