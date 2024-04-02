from dataclasses import dataclass

from seedwork.domain.factories import Factory
from usuarios.domain.events import UsuarioCreated
from usuarios.domain.repositories import UsuarioRepository
from usuarios.infrastructure.exceptions import InvalidRepositoryFactoryException
from usuarios.infrastructure.repositories import UsuariosRepositoryPostgreSQL
from usuarios.infrastructure.schema.v1.mappers import (
    UsuarioCreatedIntegrationEventMapper,
)


@dataclass
class RepositoryFactory(Factory):
    def create(self, obj: type):
        if obj == UsuarioRepository.__class__:
            return UsuariosRepositoryPostgreSQL()
        else:
            raise InvalidRepositoryFactoryException()


class IntegrationMessageFactory(Factory):
    def create(self, event: any) -> any:
        if type(event) is UsuarioCreated:
            mapper = UsuarioCreatedIntegrationEventMapper()
            return mapper.external_to_message(event)
        else:
            raise InvalidRepositoryFactoryException()
