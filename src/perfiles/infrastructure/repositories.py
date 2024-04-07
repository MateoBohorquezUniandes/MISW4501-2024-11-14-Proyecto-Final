from perfiles.domain.entities import (
    PerfilAlimenticio,
    PerfilDemografico,
    PerfilDeportivo,
)
from perfiles.domain.factories import PerfilFactory
from perfiles.domain.repositories import (
    PerfilAlimenticioRepository,
    PerfilDemograficoRepository,
    PerfilDeportivoRepository,
)
from perfiles.infrastructure.db import db
from perfiles.infrastructure.dtos import PerfilAlimenticio as PerfilAlimenticioDTO
from perfiles.infrastructure.dtos import PerfilDemografico as PerfilDemograficoDTO
from perfiles.infrastructure.dtos import PerfilDeportivo as PerfilDeportivoDTO
from perfiles.infrastructure.mappers import (
    PerfilAlimenticioMapper,
    PerfilDemograficoMapper,
    PerfilDeportivoMapper,
)


class PerfilDemograficoRepositoryPostgreSQL(PerfilDemograficoRepository):
    def __init__(self):
        self._perfil_demografico_factory: PerfilFactory = PerfilFactory()

    @property
    def fabrica_perfil_demografico(self):
        return self._perfil_demografico_factory

    def get_all(self) -> list[PerfilDemografico]:
        perfiles_dto = db.session.query(PerfilDemograficoDTO).all()
        return [
            self.fabrica_perfil_demografico.create(dto, PerfilDemograficoMapper())
            for dto in perfiles_dto
        ]

    def get(self, tipo_identificacion: str, identificacion: str) -> PerfilDemografico:
        deportista_dto = (
            db.session.query(PerfilDemograficoDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
            .one()
        )
        return self.fabrica_perfil_demografico.create(
            deportista_dto, PerfilDemograficoMapper()
        )

    def append(self, deportista: PerfilDemografico):
        deportista_dto = self.fabrica_perfil_demografico.create(
            deportista, PerfilDemograficoMapper()
        )
        db.session.add(deportista_dto)

    def delete(self, tipo_identificacion: str, identificacion: str):
        query = db.session.query(PerfilDemograficoDTO)
        if all([tipo_identificacion, identificacion]):
            query = query.filter_by(tipo_identificacion=tipo_identificacion).filter_by(
                identificacion=identificacion
            )
        query.delete()

    def update(self):
        pass


class PerfilDeportivoRepositoryPostgreSQL(PerfilDeportivoRepository):
    def __init__(self):
        self._perfil_demografico_factory: PerfilFactory = PerfilFactory()

    @property
    def fabrica_perfil_demografico(self):
        return self._perfil_demografico_factory

    def get_all(self) -> list[PerfilDeportivo]:
        perfiles_dto = db.session.query(PerfilDeportivoDTO).all()
        return [
            self.fabrica_perfil_demografico.create(dto, PerfilDeportivoMapper())
            for dto in perfiles_dto
        ]

    def get(self, tipo_identificacion: str, identificacion: str) -> PerfilDeportivo:
        deportista_dto = (
            db.session.query(PerfilDeportivoDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
            .one()
        )
        return self.fabrica_perfil_demografico.create(
            deportista_dto, PerfilDeportivoMapper()
        )

    def append(self, deportista: PerfilDeportivo):
        deportista_dto = self.fabrica_perfil_demografico.create(
            deportista, PerfilDeportivoMapper()
        )
        db.session.add(deportista_dto)

    def delete(self, tipo_identificacion: str, identificacion: str):
        query = db.session.query(PerfilDeportivoDTO)
        if all([tipo_identificacion, identificacion]):
            query = query.filter_by(tipo_identificacion=tipo_identificacion).filter_by(
                identificacion=identificacion
            )
        query.delete()

    def update(self):
        pass


class PerfilAlimenticioRepositoryPostgreSQL(PerfilAlimenticioRepository):
    def __init__(self):
        self._perfil_demografico_factory: PerfilFactory = PerfilFactory()

    @property
    def fabrica_perfil_demografico(self):
        return self._perfil_demografico_factory

    def get_all(self) -> list[PerfilAlimenticio]:
        perfiles_dto = db.session.query(PerfilAlimenticioDTO).all()
        return [
            self.fabrica_perfil_demografico.create(dto, PerfilAlimenticioMapper())
            for dto in perfiles_dto
        ]

    def get(self, tipo_identificacion: str, identificacion: str) -> PerfilAlimenticio:
        deportista_dto = (
            db.session.query(PerfilAlimenticioDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
            .one()
        )
        return self.fabrica_perfil_demografico.create(
            deportista_dto, PerfilAlimenticioMapper()
        )

    def append(self, deportista: PerfilAlimenticio):
        deportista_dto = self.fabrica_perfil_demografico.create(
            deportista, PerfilAlimenticioMapper()
        )
        db.session.add(deportista_dto)

    def delete(self, tipo_identificacion: str, identificacion: str):
        query = db.session.query(PerfilAlimenticioDTO)
        if all([tipo_identificacion, identificacion]):
            query = query.filter_by(tipo_identificacion=tipo_identificacion).filter_by(
                identificacion=identificacion
            )
        query.delete()

    def update(self):
        pass
