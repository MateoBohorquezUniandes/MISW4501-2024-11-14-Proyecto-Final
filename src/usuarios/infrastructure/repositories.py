from uuid import UUID

from usuarios.infrastructure.dtos import Usuario as UsuarioDTO
from usuarios.domain.entities import Usuario
from usuarios.domain.factories import UsuarioFactory
from usuarios.domain.repositories import UsuarioRepository
from usuarios.infrastructure.db import db
from usuarios.infrastructure.mappers import UsuarioMapper


class UsuariosRepositoryPostgreSQL(UsuarioRepository):
    def __init__(self):
        self._usuario_factory: UsuarioFactory = UsuarioFactory()

    @property
    def fabrica_usuarios(self):
        return self._usuario_factory

    def get_all(self) -> list[Usuario]:
        usuarios_dto = db.session.query(UsuarioDTO).all()
        return [
            self.fabrica_usuarios.create(dto, UsuarioMapper()) for dto in usuarios_dto
        ]

    def get(self, tipo_identificacion: str, identificacion: str, rol: str) -> Usuario:
        usuario_dto = (
            db.session.query(UsuarioDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
            .filter_by(rol=rol)
            .one()
        )
        return self.fabrica_usuarios.create(usuario_dto, UsuarioMapper())

    def append(self, usuario: Usuario):
        usuario_dto = self.fabrica_usuarios.create(usuario, UsuarioMapper())
        db.session.add(usuario_dto)

    def delete(self):
        pass

    def update(self):
        pass
