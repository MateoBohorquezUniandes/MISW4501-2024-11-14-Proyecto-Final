from typing import Union

from eventos.domain.repositories import EventoRepository
from eventos.domain.factories import EventoFactoy
from eventos.domain.entities import Evento
from eventos.infrastructure.dtos import Evento as EventoDto
from eventos.infrastructure.mappers import EventoMapper
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
