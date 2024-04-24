from perfiles.domain.entities import (
    HabitoDeportivo,
    PerfilAlimenticio,
    PerfilDemografico,
    PerfilDeportivo,
    Molestia,
)
from perfiles.domain.factories import PerfilFactory
from perfiles.domain.repositories import (
    HabitoDeportivoRepository,
    PerfilAlimenticioRepository,
    PerfilDemograficoRepository,
    PerfilDeportivoRepository,
    MolestiaRepository,
)
from perfiles.infrastructure.db import db
from perfiles.infrastructure.dtos import PerfilAlimenticio as PerfilAlimenticioDTO
from perfiles.infrastructure.dtos import PerfilDemografico as PerfilDemograficoDTO
from perfiles.infrastructure.dtos import PerfilDeportivo as PerfilDeportivoDTO
from perfiles.infrastructure.mappers import (
    HabitoDeportivoMapper,
    PerfilAlimenticioMapper,
    PerfilDemograficoMapper,
    PerfilDeportivoMapper,
    MolestiaMapper,
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
        perfil_dto = (
            db.session.query(PerfilDemograficoDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
            .one()
        )
        return self.fabrica_perfil_demografico.create(
            perfil_dto, PerfilDemograficoMapper()
        )

    def append(self, perfil: PerfilDemografico):
        perfil_dto = self.fabrica_perfil_demografico.create(
            perfil, PerfilDemograficoMapper()
        )
        db.session.add(perfil_dto)

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
        perfil_dto = (
            db.session.query(PerfilDeportivoDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
            .one()
        )
        return self.fabrica_perfil_demografico.create(
            perfil_dto, PerfilDeportivoMapper()
        )

    def append(self, perfil: PerfilDeportivo):
        perfil_dto = self.fabrica_perfil_demografico.create(
            perfil, PerfilDeportivoMapper()
        )
        db.session.add(perfil_dto)

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
        perfil_dto = (
            db.session.query(PerfilAlimenticioDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
            .one()
        )
        return self.fabrica_perfil_demografico.create(
            perfil_dto, PerfilAlimenticioMapper()
        )

    def append(self, perfil: PerfilAlimenticio):
        perfil_dto = self.fabrica_perfil_demografico.create(
            perfil, PerfilAlimenticioMapper()
        )
        db.session.add(perfil_dto)

    def delete(self, tipo_identificacion: str, identificacion: str):
        query = db.session.query(PerfilAlimenticioDTO)
        if all([tipo_identificacion, identificacion]):
            query = query.filter_by(tipo_identificacion=tipo_identificacion).filter_by(
                identificacion=identificacion
            )
        query.delete()

    def update(self):
        pass


class HabitoDeportivoRepositoryPostgreSQL(HabitoDeportivoRepository):
    def __init__(self):
        self._habito_deportivo_factory: PerfilFactory = PerfilFactory()

    @property
    def fabrica_habito_deportivo_factory(self):
        return self._habito_deportivo_factory

    def get_all(self) -> list[HabitoDeportivo]:
        pass

    def get(self, tipo_identificacion: str, identificacion: str) -> HabitoDeportivo:
        pass

    def append(self, habito: HabitoDeportivo):
        habito_dto = self._habito_deportivo_factory.create(
            habito, HabitoDeportivoMapper()
        )
        db.session.add(habito_dto)

    def delete(self, tipo_identificacion: str, identificacion: str):
        pass

    def update(self):
        pass


class MolestiaRepositoryPostgreSQL(MolestiaRepository):
    def __init__(self):
        self._molestia_factory: PerfilFactory = PerfilFactory()

    @property
    def fabrica_molestia_factory(self):
        return self._molestia_factory

    def get_all(self) -> list[Molestia]:
        pass

    def get(self, tipo_identificacion: str, identificacion: str) -> Molestia:
        pass

    def append(self, molestia: Molestia):
        molestia_dto = self._molestia_factory.create(molestia, MolestiaMapper())
        db.session.add(molestia_dto)

    def delete(self, tipo_identificacion: str, identificacion: str):
        pass

    def update(self):
        pass
