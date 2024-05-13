from typing import Union
from datetime import datetime

from eventos.domain.repositories import EventoAsociadoRepository, EventoRepository
from eventos.domain.factories import EventoFactoy
from eventos.domain.entities import Evento
from eventos.domain.value_objects import EventoAsociado
from eventos.infrastructure.dtos import Evento as EventoDto
from eventos.infrastructure.dtos import EventoAsociado as EventoAsociadoDTO
from eventos.infrastructure.mappers import EventoAsociadoMapper, EventoMapper
from eventos.infrastructure.db import db


class EventoRepositoryPostgreSQL(EventoRepository):
    def __init__(self):
        self.evento_factory: EventoFactoy = EventoFactoy()

    @property
    def fabrica_evento_factory(self):
        return self.evento_factory

    def get_all(
        self, lugar: str = None, fecha: str = None, nivel: str = None, as_entity=True
    ) -> Union[list[Evento], list[EventoDto]]:
        query = db.session.query(EventoDto)

        if lugar:
            query = query.filter_by(lugar=lugar)
        if fecha:
            query = query.filter_by(fecha=fecha)
        if nivel:
            query = query.filter_by(nive=nivel)

        eventos_dto = query.all()
        return (
            [self.evento_factory.create(dto, EventoMapper()) for dto in eventos_dto]
            if as_entity
            else eventos_dto
        )

    def get(self) -> Evento:
        pass

    def append(self, evento: Evento):
        evento_dto = self.evento_factory.create(evento, EventoMapper())
        db.session.add(evento_dto)

    def delete(self):
        pass

    def update(self):
        pass


class EventoAsociadoRepositoryPostgreSQL(EventoAsociadoRepository):
    def __init__(self):
        self._perfil_factory: EventoFactoy = EventoFactoy()

    @property
    def perfil_factory(self):
        return self._perfil_factory

    def get_all(
        self, tipo_identificacion: str, identificacion: str, programado: bool
    ) -> list[Evento]:
        asociaciones_dto = (
            db.session.query(EventoAsociadoDTO)
            .filter_by(tipo_identificacion=tipo_identificacion)
            .filter_by(identificacion=identificacion)
        )
        timestamp = datetime.utcnow()
        asociaciones_dto = asociaciones_dto.filter(
            EventoAsociadoDTO.fecha >= timestamp
            if programado
            else EventoAsociadoDTO.fecha < timestamp
        )

        mapper = EventoMapper()
        return [
            self.perfil_factory.create(dto.evento, mapper) for dto in asociaciones_dto.all()
        ]

    def get(self, id: str) -> EventoAsociado:
        asociacion_dto = (
            db.session.query(EventoAsociadoDTO).filter_by(id_alimento=id).one()
        )
        alimento = self.perfil_factory.create(asociacion_dto.alimento, EventoMapper())
        return alimento

    def append(self, asociacion: EventoAsociado):
        asociacion_dto = self.perfil_factory.create(asociacion, EventoAsociadoMapper())
        db.session.add(asociacion_dto)

    def delete(self, id: str):
        query = db.session.query(EventoAsociadoDTO)
        if id:
            query = query.filter_by(id=id)
        query.delete()

    def update(self, asociacion: EventoAsociado):
        pass
