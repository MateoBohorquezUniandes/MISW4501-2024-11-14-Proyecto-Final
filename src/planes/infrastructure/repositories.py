from typing import Union
from planes.domain.entities import Entrenamiento, PlanEntrenamiento, UsuarioPlan
from planes.domain.factories import PlanFactory
from planes.domain.repositories import (
    EntrenamientoRepository,
    PlanEntrenamientoRepository,
    UsuarioPlanRepository,
)
from planes.infrastructure.db import db
from planes.infrastructure.dtos import PlanEntrenamiento as PlanEntrenamientoDTO
from planes.infrastructure.dtos import Entrenamiento as EntrenamientoDTO
from planes.infrastructure.dtos import UsuarioPlan as UsuarioPlanDTO
from planes.infrastructure.mappers import (
    EntrenamientoMapper,
    PlanEntrenamientoMapper,
    UsuarioPlanMapper,
)


class EntrenamientoRepositoryPostgreSQL(EntrenamientoRepository):
    def __init__(self):
        self._plan_factory: PlanFactory = PlanFactory()

    @property
    def plan_factory(self):
        return self._plan_factory

    def get_all(
        self, ids: list[str] = [], as_entity=True
    ) -> Union[list[Entrenamiento], list[EntrenamientoDTO]]:
        query = db.session.query(EntrenamientoDTO)
        if ids:
            query = query.filter(EntrenamientoDTO.id.in_(ids))

        entrenamientos_dto = query.all()
        return (
            [
                self.plan_factory.create(dto, EntrenamientoMapper())
                for dto in entrenamientos_dto
            ]
            if as_entity
            else entrenamientos_dto
        )

    def get(self, id: str, as_entity=True) -> Union[Entrenamiento, EntrenamientoDTO]:
        entrenamiento_dto = db.session.query(EntrenamientoDTO).filter_by(id=id).one()
        if as_entity:
            return self.plan_factory.create(entrenamiento_dto, EntrenamientoMapper())
        else:
            return entrenamiento_dto

    def append(self, entrenamiento: Entrenamiento):
        entrenamiento_dto: EntrenamientoDTO = self.plan_factory.create(
            entrenamiento, EntrenamientoMapper()
        )
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
        plan_dto: PlanEntrenamientoDTO = self.get(str(plan.id), as_entity=False)
        entrenamientos_dto = EntrenamientoRepositoryPostgreSQL().get_all(
            ids=[str(e.id) for e in plan.entrenamientos], as_entity=False
        )
        plan_dto.entrenamientos.extend(entrenamientos_dto)


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
        self, tipo_identificacion: str, identificacion: str, as_entity=True
    ) -> Union[UsuarioPlan, UsuarioPlanDTO]:
        usuario_dto = (
            db.session.query(UsuarioPlanDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
            .one()
        )
        if as_entity:
            return self.plan_factory.create(usuario_dto, UsuarioPlanMapper())
        else:
            return usuario_dto

    def append(self, usuario: UsuarioPlan, deporte: str = None, exigencia: str = None):
        usuario_dto: UsuarioPlanDTO = self.plan_factory.create(
            usuario, UsuarioPlanMapper()
        )
        planes_dto = PlanEntrenamientoRepositoryPostgreSQL().get_all(
            nivel_exigencia=exigencia, deporte_objetivo=deporte, as_entity=False
        )
        usuario_dto.planes.extend(planes_dto)
        db.session.add(usuario_dto)

    def delete(self, tipo_identificacion: str, identificacion: str):
        query = db.session.query(UsuarioPlanDTO)
        if all([tipo_identificacion, identificacion]):
            query = query.filter_by(tipo_identificacion=tipo_identificacion).filter_by(
                identificacion=identificacion
            )
        query.delete()

    def update(self, usuario: UsuarioPlan, planes: list[PlanEntrenamientoDTO]):
        usuario_dto: UsuarioPlanDTO = self.get(
            usuario.tipo_identificacion, usuario.identificacion, as_entity=False
        )
        usuario_dto.planes.extend(planes)

    def relate_plan_entrenamiento(self):
        pass
