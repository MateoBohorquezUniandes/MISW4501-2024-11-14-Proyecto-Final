from dataclasses import dataclass

from perfiles.domain.entities import (
    HabitoDeportivo,
    PerfilAlimenticio,
    PerfilDemografico,
    PerfilDeportivo,
    Molestia,
)
from perfiles.domain.events import PerfilDemograficoModified
from perfiles.infrastructure.exceptions import InvalidRepositoryFactoryException
from perfiles.infrastructure.repositories import (
    HabitoDeportivoRepositoryPostgreSQL,
    PerfilAlimenticioRepositoryPostgreSQL,
    PerfilDemograficoRepositoryPostgreSQL,
    PerfilDeportivoRepositoryPostgreSQL,
    MolestiaRepositoryPostgreSQL,
)
from perfiles.infrastructure.schema.v1.mappers import (
    DemograficoModifiedIntegrationEventMapper,
)
from seedwork.domain.factories import Factory


@dataclass
class RepositoryFactory(Factory):
    def create(self, obj):
        if isinstance(obj, PerfilDemografico) or obj == PerfilDemografico:
            return PerfilDemograficoRepositoryPostgreSQL()
        elif isinstance(obj, PerfilDeportivo) or obj == PerfilDeportivo:
            return PerfilDeportivoRepositoryPostgreSQL()
        elif isinstance(obj, PerfilAlimenticio) or obj == PerfilAlimenticio:
            return PerfilAlimenticioRepositoryPostgreSQL()
        elif isinstance(obj, HabitoDeportivo) or obj == HabitoDeportivo:
            return HabitoDeportivoRepositoryPostgreSQL()
        elif isinstance(obj, Molestia) or obj == Molestia:
            return MolestiaRepositoryPostgreSQL()
        else:
            raise InvalidRepositoryFactoryException()


class IntegrationMessageFactory(Factory):
    def create(self, event: any) -> any:
        if type(event) is PerfilDemograficoModified:
            mapper = DemograficoModifiedIntegrationEventMapper()
            return mapper.external_to_message(event)
        else:
            raise InvalidRepositoryFactoryException()
