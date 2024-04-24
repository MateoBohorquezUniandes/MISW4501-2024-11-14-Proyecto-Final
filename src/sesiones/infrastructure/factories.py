from dataclasses import dataclass

from seedwork.domain.factories import Factory
from sesiones.domain.entities import SesionDeportiva
from sesiones.domain.events import SesionEnded
from sesiones.infrastructure.exceptions import InvalidRepositoryFactoryException
from sesiones.infrastructure.repositories import SesionDeportivaRepositoryPostgreSQL
from sesiones.infrastructure.schema.mappers import SesionEndedIntegrationEventMapper


@dataclass
class RepositoryFactory(Factory):
    def create(self, obj):
        if isinstance(obj, SesionDeportiva) or obj == SesionDeportiva:
            return SesionDeportivaRepositoryPostgreSQL()
        else:
            raise InvalidRepositoryFactoryException()


class IntegrationMessageFactory(Factory):
    def create(self, event: any) -> any:
        if isinstance(event, SesionEnded):
            mapper = SesionEndedIntegrationEventMapper()
            return mapper.external_to_message(event)
        else:
            raise InvalidRepositoryFactoryException()
