from perfiles.domain.entities import (
    Alimento,
    HabitoDeportivo,
    PerfilAlimenticio,
    PerfilDemografico,
    PerfilDeportivo,
    Molestia,
)
from perfiles.domain.factories import PerfilFactory
from perfiles.domain.repositories import (
    AlimentoAsociadoRepository,
    AlimentoRepository,
    HabitoDeportivoRepository,
    PerfilAlimenticioRepository,
    PerfilDemograficoRepository,
    PerfilDeportivoRepository,
    MolestiaRepository,
)
from perfiles.domain.value_objects import AlimentoAsociado
from perfiles.infrastructure.db import db
from perfiles.infrastructure.dtos import PerfilAlimenticio as PerfilAlimenticioDTO
from perfiles.infrastructure.dtos import PerfilDemografico as PerfilDemograficoDTO
from perfiles.infrastructure.dtos import PerfilDeportivo as PerfilDeportivoDTO
from perfiles.infrastructure.dtos import Alimento as AlimentoDTO
from perfiles.infrastructure.dtos import AlimentoAsociado as AlimentoAsociadoDTO
from perfiles.infrastructure.mappers import (
    AlimentoAsociadoMapper,
    AlimentoMapper,
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

    def get(
        self, tipo_identificacion: str, identificacion: str, as_entity=True
    ) -> PerfilDemografico:
        perfil_dto = (
            db.session.query(PerfilDemograficoDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
            .one()
        )
        return (
            self.fabrica_perfil_demografico.create(
                perfil_dto, PerfilDemograficoMapper()
            )
            if as_entity
            else perfil_dto
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

    def update(self, perfil: PerfilDemografico):
        perfil_dto = self.get(
            perfil.tipo_identificacion, perfil.identificacion, as_entity=False
        )
        perfil_dto = self.fabrica_perfil_demografico.create(
            perfil, PerfilDemograficoMapper(), perfil_dto=perfil_dto
        )


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
        self._perfil_factory: PerfilFactory = PerfilFactory()

    @property
    def perfil_factory(self):
        return self._perfil_factory

    def get_all(self) -> list[PerfilAlimenticio]:
        perfiles_dto = db.session.query(PerfilAlimenticioDTO).all()
        return [
            self.perfil_factory.create(dto, PerfilAlimenticioMapper())
            for dto in perfiles_dto
        ]

    def get(
        self, tipo_identificacion: str, identificacion: str, as_entity=True
    ) -> PerfilAlimenticio:
        perfil_dto = (
            db.session.query(PerfilAlimenticioDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
            .one()
        )
        return (
            self.perfil_factory.create(perfil_dto, PerfilAlimenticioMapper())
            if as_entity
            else perfil_dto
        )

    def append(self, perfil: PerfilAlimenticio):
        perfil_dto = self.perfil_factory.create(perfil, PerfilAlimenticioMapper())
        db.session.add(perfil_dto)

    def delete(self, tipo_identificacion: str, identificacion: str):
        query = db.session.query(PerfilAlimenticioDTO)
        if all([tipo_identificacion, identificacion]):
            query = query.filter_by(tipo_identificacion=tipo_identificacion).filter_by(
                identificacion=identificacion
            )
        query.delete()

    def update(self, perfil: PerfilAlimenticio):
        perfil_dto: PerfilAlimenticioDTO = self.get(
            perfil.tipo_identificacion, perfil.identificacion, as_entity=False
        )
        perfil_dto.tipo_alimentacion = perfil.tipo_alimentacion


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


class AlimentoRepositoryPostgreSQL(AlimentoRepository):
    def __init__(self):
        self._perfil_factory: PerfilFactory = PerfilFactory()

    @property
    def perfil_factory(self):
        return self._perfil_factory

    def get_all(self) -> list[Alimento]:
        alimentos_dto = db.session.query(AlimentoDTO).all()
        mapper = AlimentoMapper()
        return [self.perfil_factory.create(dto, mapper) for dto in alimentos_dto]

    def get(self, id: str) -> Alimento:
        alimento_dto = db.session.query(AlimentoDTO).filter_by(id=id).one()
        return self.perfil_factory.create(alimento_dto, AlimentoMapper())

    def append(self, alimento: Alimento):
        alimento_dto = self.perfil_factory.create(alimento, AlimentoMapper())
        db.session.add(alimento_dto)

    def associate(self, asociacion: AlimentoAsociado):
        asociacion_dto = self.perfil_factory.create(
            asociacion, AlimentoAsociadoMapper()
        )
        db.session.add(asociacion_dto)

    def delete(self, id: str):
        query = db.session.query(AlimentoDTO)
        if id:
            query = query.filter_by(id=id)
        query.delete()

    def update(self, alimento: Alimento):
        pass


class AlimentoAsociadoRepositoryPostgreSQL(AlimentoAsociadoRepository):
    def __init__(self):
        self._perfil_factory: PerfilFactory = PerfilFactory()

    @property
    def perfil_factory(self):
        return self._perfil_factory

    def get_all(self, tipo_identificacion: str, identificacion: str) -> list[Alimento]:
        asociaciones_dto = (
            db.session.query(AlimentoAsociadoDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
            .all()
        )
        alimentos, mapper = [], AlimentoMapper()
        for pos, dto in enumerate(asociaciones_dto):
            alimentos.append(self.perfil_factory.create(dto.alimento, mapper))
            alimentos[pos].tipo = dto.tipo

        return alimentos

    def get(self, id: str) -> AlimentoAsociado:
        asociacion_dto = (
            db.session.query(AlimentoAsociadoDTO).filter_by(id_alimento=id).one()
        )
        alimento = self.perfil_factory.create(asociacion_dto.alimento, AlimentoMapper())
        alimento.tipo = asociacion_dto.tipo
        return alimento

    def append(self, asociacion: AlimentoAsociado):
        asociacion_dto = self.perfil_factory.create(
            asociacion, AlimentoAsociadoMapper()
        )
        db.session.add(asociacion_dto)

    def delete(self, id: str):
        query = db.session.query(AlimentoAsociadoDTO)
        if id:
            query = query.filter_by(id=id)
        query.delete()

    def update(self, asociacion: AlimentoAsociado):
        pass
