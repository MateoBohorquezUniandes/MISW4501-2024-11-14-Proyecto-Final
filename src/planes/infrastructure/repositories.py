from typing import Union

from planes.domain.entities import (
    Entrenamiento,
    GrupoAlimenticio,
    PlanEntrenamiento,
    RutinaAlimentacion,
    UsuarioPlan,
)
from planes.domain.factories import PlanFactory
from planes.domain.repositories import (
    EntrenamientoRepository,
    GrupoAlimenticioRepository,
    PlanEntrenamientoRepository,
    RutinaAlimentacionRepository,
    UsuarioPlanRepository,
)
from planes.infrastructure.db import db
from planes.infrastructure.dtos import Entrenamiento as EntrenamientoDTO
from planes.infrastructure.dtos import GrupoAlimenticio as GrupoAlimenticioDTO
from planes.infrastructure.dtos import PlanEntrenamiento as PlanEntrenamientoDTO
from planes.infrastructure.dtos import RutinaAlimentacion as RutinaAlimentacionDTO
from planes.infrastructure.dtos import UsuarioPlan as UsuarioPlanDTO
from planes.infrastructure.mappers import (
    EntrenamientoMapper,
    GrupoAlimenticioMapper,
    PlanEntrenamientoMapper,
    RutinaAlimentacionMapper,
    UsuarioPlanMapper,
)


class EntrenamientoRepositoryPostgreSQL(EntrenamientoRepository):
    def __init__(self):
        self._plan_factory: PlanFactory = PlanFactory()

    @property
    def plan_factory(self):
        return self._plan_factory

    def get_all(self, plan_id: str = None) -> list[Entrenamiento]:
        query = db.session.query(EntrenamientoDTO)
        if plan_id:
            query = query.filter_by(plan_id=plan_id)

        return [
            self.plan_factory.create(dto, EntrenamientoMapper()) for dto in query.all()
        ]

    def get(self, id: str, as_entity=True) -> Union[Entrenamiento, EntrenamientoDTO]:
        entrenamiento_dto = db.session.query(EntrenamientoDTO).filter_by(id=id).one()
        if as_entity:
            return self.plan_factory.create(entrenamiento_dto, EntrenamientoMapper())
        else:
            return entrenamiento_dto

    def append(self, entrenamiento: Entrenamiento, plan_id: str):
        entrenamiento_dto: EntrenamientoDTO = self.plan_factory.create(
            entrenamiento, EntrenamientoMapper()
        )
        entrenamiento_dto.plan_id = plan_id
        db.session.add(entrenamiento_dto)

    def delete(self, id: str):
        query = db.session.query(EntrenamientoDTO)
        if id:
            query = query.filter_by(id=id)
        query.delete()

    def update(self):
        pass


class PlanEntrenamientoRepositoryPostgreSQL(PlanEntrenamientoRepository):
    def __init__(self):
        self._plan_factory: PlanFactory = PlanFactory()

    @property
    def plan_factory(self):
        return self._plan_factory

    def get_all(
        self, nivel_exigencia: str = None, deporte_objetivo: str = None, as_entity=True
    ) -> Union[list[PlanEntrenamiento], list[PlanEntrenamientoDTO]]:
        query = db.session.query(PlanEntrenamientoDTO)
        if nivel_exigencia:
            query = query.filter_by(nivel_exigencia=nivel_exigencia)
        if deporte_objetivo:
            query = query.filter_by(deporte_objetivo=deporte_objetivo)

        planes_dto = query.all()
        return (
            [
                self.plan_factory.create(dto, PlanEntrenamientoMapper())
                for dto in planes_dto
            ]
            if as_entity
            else planes_dto
        )

    def get(
        self, id: str, as_entity=True
    ) -> Union[PlanEntrenamiento, PlanEntrenamientoDTO]:
        plan_dto = db.session.query(PlanEntrenamientoDTO).filter_by(id=id).one()
        if as_entity:
            return self.plan_factory.create(plan_dto, PlanEntrenamientoMapper())
        else:
            return plan_dto

    def append(self, plan: PlanEntrenamiento):
        plan_dto = self.plan_factory.create(plan, PlanEntrenamientoMapper())
        db.session.add(plan_dto)

    def delete(self, id: str):
        query = db.session.query(PlanEntrenamientoDTO)
        if id:
            query = query.filter_by(id=id)
        query.delete()

    def update(self, plan: PlanEntrenamiento):
        pass


class UsuarioPlanRepositoryPostgreSQL(UsuarioPlanRepository):
    def __init__(self):
        self._plan_factory: PlanFactory = PlanFactory()

    @property
    def plan_factory(self):
        return self._plan_factory

    def get_all(self, as_entity=True) -> Union[list[UsuarioPlan], list[UsuarioPlanDTO]]:
        usuarios_dto = db.session.query(UsuarioPlanDTO).all()
        return (
            [self.plan_factory.create(dto, UsuarioPlanMapper()) for dto in usuarios_dto]
            if as_entity
            else usuarios_dto
        )

    def get(
        self,
        tipo_identificacion: str,
        identificacion: str,
        as_entity=True,
        raise_error=True,
    ) -> Union[UsuarioPlan, UsuarioPlanDTO]:
        usuario_dto = (
            db.session.query(UsuarioPlanDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
        )
        usuario_dto = usuario_dto.one() if raise_error else usuario_dto.first()
        if as_entity:
            return self.plan_factory.create(usuario_dto, UsuarioPlanMapper())
        else:
            return usuario_dto

    def append(self, usuario: UsuarioPlan, deporte: str = None, exigencia: str = None):
        usuario_dto = self.get(
            usuario.tipo_identificacion,
            usuario.identificacion,
            as_entity=False,
            raise_error=False,
        )
        should_add = False
        if not usuario_dto:
            should_add = True
            usuario_dto: UsuarioPlanDTO = self.plan_factory.create(
                usuario, UsuarioPlanMapper()
            )
        print(f"should add new? {should_add}")
        self.update(usuario_dto, deporte=deporte, exigencia=exigencia)

        if should_add:
            db.session.add(usuario_dto)

    def delete(self, tipo_identificacion: str, identificacion: str):
        query = db.session.query(UsuarioPlanDTO)
        if all([tipo_identificacion, identificacion]):
            query = query.filter_by(tipo_identificacion=tipo_identificacion).filter_by(
                identificacion=identificacion
            )
        query.delete()

    def update(
        self, usuario_dto: UsuarioPlanDTO, deporte: str = None, exigencia: str = None
    ):
        planes_dto = PlanEntrenamientoRepositoryPostgreSQL().get_all(
            nivel_exigencia=exigencia, deporte_objetivo=deporte, as_entity=False
        )
        planes_asociados = [p.id for p in usuario_dto.planes]
        usuario_dto.planes.extend(
            [p for p in planes_dto if p.id not in planes_asociados]
        )


class GrupoAlimenticioRepositoryPostgreSQL(GrupoAlimenticioRepository):
    def __init__(self):
        self._plan_factory: PlanFactory = PlanFactory()

    @property
    def plan_factory(self):
        return self._plan_factory

    def get_all(self, rutina_id: str) -> list[GrupoAlimenticioDTO]:
        query = db.session.query(GrupoAlimenticioDTO).filter_by(rutina_id=rutina_id)
        return [
            self.plan_factory.create(dto, GrupoAlimenticioMapper())
            for dto in query.all()
        ]

    def get(
        self, id: str, as_entity=True
    ) -> Union[GrupoAlimenticio, GrupoAlimenticioDTO]:
        grupo_dto = db.session.query(GrupoAlimenticioDTO).filter_by(id=id).one()
        if as_entity:
            return self.plan_factory.create(grupo_dto, GrupoAlimenticioMapper())
        else:
            return grupo_dto

    def append(self, grupo: GrupoAlimenticio, rutina_id: str):
        grupo_dto: GrupoAlimenticioDTO = self.plan_factory.create(
            grupo, GrupoAlimenticioMapper()
        )
        grupo_dto.rutina_id = rutina_id
        db.session.add(grupo_dto)

    def delete(self, id: str):
        query = db.session.query(GrupoAlimenticioDTO)
        if id:
            query = query.filter_by(id=id)
        query.delete()

    def update(self, grupo: GrupoAlimenticio):
        pass


class RutinaAlimentacionRepositoryPostgreSQL(RutinaAlimentacionRepository):
    def __init__(self):
        self._plan_factory: PlanFactory = PlanFactory()

    @property
    def plan_factory(self):
        return self._plan_factory

    def get_all(
        self, tipo_alimentacion: str = None, deporte: str = None
    ) -> list[RutinaAlimentacion]:
        query = db.session.query(RutinaAlimentacionDTO)

        if tipo_alimentacion:
            query = query.filter_by(tipo_alimentacion=tipo_alimentacion)
        if deporte:
            query = query.filter_by(deporte=deporte)

        return [
            self.plan_factory.create(dto, RutinaAlimentacionMapper())
            for dto in query.all()
        ]

    def get(
        self, id: str, as_entity=True
    ) -> Union[RutinaAlimentacion, RutinaAlimentacionDTO]:
        rutina_dto = db.session.query(RutinaAlimentacionDTO).filter_by(id=id).one()
        if as_entity:
            return self.plan_factory.create(rutina_dto, RutinaAlimentacionMapper())
        else:
            return rutina_dto

    def append(self, plan: RutinaAlimentacion):
        rutina_dto = self.plan_factory.create(plan, RutinaAlimentacionMapper())
        db.session.add(rutina_dto)

    def delete(self, id: str):
        query = db.session.query(RutinaAlimentacionDTO)
        if id:
            query = query.filter_by(id=id)
        query.delete()

    def update(self, rutina: RutinaAlimentacion):
        pass
