from dataclasses import dataclass

from perfiles.domain.entities import (
    PerfilAlimenticio,
    PerfilDemografico,
    PerfilDeportivo,
)
from perfiles.domain.events import PerfilDemograficoCreated
from perfiles.infrastructure.exceptions import InvalidRepositoryFactoryException
from perfiles.infrastructure.repositories import (
    PerfilAlimenticioRepositoryPostgreSQL,
    PerfilDemograficoRepositoryPostgreSQL,
    PerfilDeportivoRepositoryPostgreSQL,
)
from perfiles.infrastructure.schema.v1.mappers import (
    DemografiaCreatedIntegrationEventMapper,
)
from seedwork.domain.factories import Factory


@dataclass
class RepositoryFactory(Factory):
    def create(self, obj):
        if isinstance(obj, PerfilDemografico):
            return PerfilDemograficoRepositoryPostgreSQL()
        elif isinstance(obj, PerfilDeportivo):
            return PerfilDeportivoRepositoryPostgreSQL()
        elif isinstance(obj, PerfilAlimenticio):
            return PerfilAlimenticioRepositoryPostgreSQL()
        else:
            raise InvalidRepositoryFactoryException()


class IntegrationMessageFactory(Factory):
    def create(self, event: any) -> any:
        if type(event) is PerfilDemograficoCreated:
            mapper = DemografiaCreatedIntegrationEventMapper()
            return mapper.external_to_message(event)
        else:
            raise InvalidRepositoryFactoryException()
