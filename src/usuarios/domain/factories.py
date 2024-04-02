from dataclasses import dataclass
from typing import Union

from seedwork.domain.entities import Entity
from seedwork.domain.events import DomainEvent
from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Mapper, UnidirectionalMapper
from usuarios.domain.entities import Usuario
from usuarios.domain.exceptions import (
    InvalidLoginFactoryException,
    InvalidPasswordFactoryException,
    InvalidUsuarioFactoryException,
)
from usuarios.domain.rules import ValidContrasena, ValidIdentificacion, ValidUsuario
from usuarios.domain.value_objects import Contrasena, LoginRequest


@dataclass
class _UsuarioFactory(Factory):
    def create(self, obj: any, mapper: Mapper = None) -> Usuario:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)

        usuario: Usuario = mapper.dto_to_entity(obj)
        self.validate_rule(ValidUsuario(usuario))
        return usuario

@dataclass
class UsuarioFactory(Factory):
    def create(self, obj: any, mapper: Mapper):
        if mapper.type() == Usuario.__class__:
            usuario_factory = _UsuarioFactory()
            return usuario_factory.create(obj, mapper)

        else:
            raise InvalidUsuarioFactoryException()


@dataclass
class ContrasenaFactory(Factory):
    def create(
        self, contrasena: str, salt: str = None, mapper: UnidirectionalMapper = None
    ) -> Contrasena:
        if mapper.type() == Contrasena.__class__:
            self.validate_rule(ValidContrasena(contrasena))
            contrasena = mapper.map(contrasena, salt)
            return contrasena
        else:
            raise InvalidPasswordFactoryException()

@dataclass
class LoginFactory(Factory):
    def create(self, obj: any, mapper: Mapper):
        if mapper.type() == LoginRequest.__class__:
            login_request: LoginRequest = mapper.map(obj)
            self.validate_rule(ValidIdentificacion(login_request.identificacion))
            return login_request
        else:
            raise InvalidLoginFactoryException()
