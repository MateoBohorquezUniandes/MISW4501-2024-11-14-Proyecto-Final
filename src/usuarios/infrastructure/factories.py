from dataclasses import dataclass

from seedwork.domain.factories import Factory
from usuarios.domain.entities import Deportista, Organizador, Socio
from usuarios.domain.events import UsuarioCreated
from usuarios.domain.repositories import DeportistaRepository
from usuarios.infrastructure.exceptions import InvalidRepositoryFactoryException
from usuarios.infrastructure.repositories import (
    DeportistaRepositoryPostgreSQL,
    OrganizadorRepositoryPostgreSQL,
    SocioRepositoryPostgreSQL,
)
from usuarios.infrastructure.schema.v1.mappers import (
    UsuarioCreatedIntegrationEventMapper,
)


@dataclass
class RepositoryFactory(Factory):
    def create(self, obj):
        if isinstance(obj, Deportista):
            return DeportistaRepositoryPostgreSQL()
        elif isinstance(obj, Organizador):
            return OrganizadorRepositoryPostgreSQL()
        elif isinstance(obj, Socio):
            return SocioRepositoryPostgreSQL()
        else:
            raise InvalidRepositoryFactoryException()


class IntegrationMessageFactory(Factory):
    def create(self, event: any) -> any:
        if type(event) is UsuarioCreated:
            mapper = UsuarioCreatedIntegrationEventMapper()
            return mapper.external_to_message(event)
        else:
            raise InvalidRepositoryFactoryException()
