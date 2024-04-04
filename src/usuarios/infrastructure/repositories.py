from usuarios.domain.entities import Deportista, Organizador, Socio
from usuarios.domain.factories import UsuarioFactory
from usuarios.domain.repositories import (
    DeportistaRepository,
    OrganizadorRepository,
    SocioRepository,
)
from usuarios.infrastructure.db import db
from usuarios.infrastructure.dtos import Deportista as DeportistaDTO
from usuarios.infrastructure.dtos import Organizador as OrganizadorDTO
from usuarios.infrastructure.dtos import Socio as SocioDTO
from usuarios.infrastructure.mappers import (
    DeportistaMapper,
    OrganizadorMapper,
    SocioMapper,
)


class DeportistaRepositoryPostgreSQL(DeportistaRepository):
    def __init__(self):
        self._deportista_factory: UsuarioFactory = UsuarioFactory()

    @property
    def fabrica_deportistas(self):
        return self._deportista_factory

    def get_all(self) -> list[Deportista]:
        deportistas_dto = db.session.query(DeportistaDTO).all()
        return [
            self.fabrica_deportistas.create(dto, DeportistaMapper())
            for dto in deportistas_dto
        ]

    def get(
        self, tipo_identificacion: str, identificacion: str, rol: str
    ) -> Deportista:
        deportista_dto = (
            db.session.query(DeportistaDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
            .filter_by(rol=rol)
            .one()
        )
        return self.fabrica_deportistas.create(deportista_dto, DeportistaMapper())

    def append(self, deportista: Deportista):
        deportista_dto = self.fabrica_deportistas.create(deportista, DeportistaMapper())
        db.session.add(deportista_dto)

    def delete(self, tipo_identificacion: str, identificacion: str, rol: str):
        query = db.session.query(DeportistaDTO)
        if all([tipo_identificacion, identificacion, rol]):
            query = (
                query.filter_by(tipo_identificacion=tipo_identificacion)
                .filter_by(identificacion=identificacion)
                .filter_by(rol=rol)
            )
        query.delete()

    def update(self):
        pass


class OrganizadorRepositoryPostgreSQL(OrganizadorRepository):
    def __init__(self):
        self._organizador_factory: UsuarioFactory = UsuarioFactory()

    @property
    def fabrica_organizadores(self):
        return self._organizador_factory

    def get_all(self) -> list[Organizador]:
        organizadores_dto = db.session.query(OrganizadorDTO).all()
        return [
            self.fabrica_organizadores.create(dto, OrganizadorMapper())
            for dto in organizadores_dto
        ]

    def get(
        self, tipo_identificacion: str, identificacion: str, rol: str
    ) -> Organizador:
        organizador_dto = (
            db.session.query(OrganizadorDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
            .filter_by(rol=rol)
            .one()
        )
        return self.fabrica_organizadores.create(organizador_dto, OrganizadorMapper())

    def append(self, organizador: Organizador):
        organizador_dto = self.fabrica_organizadores.create(
            organizador, OrganizadorMapper()
        )
        db.session.add(organizador_dto)

    def delete(self, tipo_identificacion: str, identificacion: str, rol: str):
        query = db.session.query(OrganizadorDTO)
        if all([tipo_identificacion, identificacion, rol]):
            query = (
                query.filter_by(tipo_identificacion=tipo_identificacion)
                .filter_by(identificacion=identificacion)
                .filter_by(rol=rol)
            )
        query.delete()

    def update(self):
        pass


class SocioRepositoryPostgreSQL(SocioRepository):
    def __init__(self):
        self._socio_factory: UsuarioFactory = UsuarioFactory()

    @property
    def fabrica_socios(self):
        return self._socio_factory

    def get_all(self) -> list[Socio]:
        socios_dto = db.session.query(SocioDTO).all()
        return [self.fabrica_socios.create(dto, SocioMapper()) for dto in socios_dto]

    def get(self, tipo_identificacion: str, identificacion: str, rol: str) -> Socio:
        socio_dto = (
            db.session.query(SocioDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
            .filter_by(rol=rol)
            .one()
        )
        return self.fabrica_socios.create(socio_dto, SocioMapper())

    def append(self, socio: Socio):
        socio_dto = self.fabrica_socios.create(socio, SocioMapper())
        db.session.add(socio_dto)

    def delete(self, tipo_identificacion: str, identificacion: str, rol: str):
        query = db.session.query(SocioDTO)
        if all([tipo_identificacion, identificacion, rol]):
            query = (
                query.filter_by(tipo_identificacion=tipo_identificacion)
                .filter_by(identificacion=identificacion)
                .filter_by(rol=rol)
            )
        query.delete()

    def update(self):
        pass
