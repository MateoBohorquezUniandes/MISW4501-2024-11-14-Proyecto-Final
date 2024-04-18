from typing import Union
from sesiones.domain.entities import SesionDeportiva
from sesiones.domain.factories import SesionFactory
from sesiones.domain.repositories import SesionDeportivaRepository
from sesiones.infrastructure.dtos import SesionDeportiva as SesionDeportivaDTO
from sesiones.infrastructure.db import db
from sesiones.infrastructure.mappers import SesionDeportivaMapper


class SesionDeportivaRepositoryPostgreSQL(SesionDeportivaRepository):
    def __init__(self):
        self._sesion_factory: SesionFactory = SesionFactory()

    @property
    def sesion_factory(self):
        return self._sesion_factory

    def get_all(
        self, tipo_identificacion: str, identificacion: str, as_entity=True
    ) -> Union[list[SesionDeportiva], list[SesionDeportivaDTO]]:
        query = db.session.query(SesionDeportivaDTO)

        if tipo_identificacion and identificacion:
            query = query.filter_by(tipo_identificacion=tipo_identificacion).filter_by(
                identificacion=identificacion
            )

        sesiones_dto = query.all()
        return (
            [
                self.sesion_factory.create(dto, SesionDeportivaMapper())
                for dto in sesiones_dto
            ]
            if as_entity
            else sesiones_dto
        )

    def get(
        self, tipo_identificacion: str, identificacion: str, id: str, as_entity=True
    ) -> Union[SesionDeportiva, SesionDeportivaDTO]:
        sesion_dto = (
            db.session.query(SesionDeportivaDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
            .filter_by(id=id)
            .one()
        )

        return (
            self.sesion_factory.create(sesion_dto, SesionDeportivaMapper())
            if as_entity
            else sesion_dto
        )

    def append(self, sesion: SesionDeportiva):
        sesion_dto: SesionDeportivaDTO = self.sesion_factory.create(
            sesion, SesionDeportivaMapper()
        )
        db.session.add(sesion_dto)

    def delete(self, id: str):
        query = db.session.query(SesionDeportivaDTO)
        if id:
            query = query.filter_by(id=id)
        query.delete()

    def update(self, sesion: SesionDeportiva):
        sesion_dto = self.get(
            sesion.tipo_identificacion,
            sesion.identificacion,
            str(sesion.id),
            as_entity=False,
        )
        sesion_dto.completed_at = sesion.completed_at
