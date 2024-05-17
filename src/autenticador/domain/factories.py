from dataclasses import asdict, dataclass

from flask_jwt_extended import create_access_token

from autenticador.domain.entities import Autenticacion
from autenticador.domain.exceptions import InvalidTokenRequestFactoryException
from autenticador.domain.rules import ValidTokenIdentity
from seedwork.domain.entities import Entity
from seedwork.domain.events import DomainEvent
from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Mapper


@dataclass
class _TokenRequestFactory(Factory):

    def create(self, obj: any, mapper: Mapper = None) -> Autenticacion:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)

        autenticacion: Autenticacion = mapper.dto_to_entity(obj)
        self.validate_rule(ValidTokenIdentity(autenticacion.identity))

        autenticacion.token.valor = create_access_token(
            identity=asdict(autenticacion.identity),
            expires_delta=autenticacion.token.expiration_delta,
        )

        return autenticacion


@dataclass
class TokenRequestFactory(Factory):
    def create(self, obj: any, mapper: Mapper) -> Autenticacion:
        if mapper.type() == Autenticacion.__class__:
            autenticacion_factory = _TokenRequestFactory()
            return autenticacion_factory.create(obj, mapper)
        else:
            raise InvalidTokenRequestFactoryException()
