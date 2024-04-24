import datetime

from uuid import UUID

from eventos.domain.entities import Evento
from eventos.domain.value_objects import EventoTipo, EventoNivel
from eventos.infrastructure.dtos import Evento as EventoDto

from seedwork.domain.repositories import Mapper


class EventoMapper(Mapper):
    def type(self) -> type:
        return Evento

    def dto_to_entity(self, dto: EventoDto) -> Evento:

        args = [UUID(dto.id)] if dto.id else []
        return Evento(
            *args,
            tipo=dto.tipo,
            fecha=str(dto.fecha.date()),
            lugar=dto.lugar,
            distancia=dto.distancia,
            nivel=dto.nivel,
            nombre=dto.nombre
        )

    def entity_to_dto(self, entity: Evento) -> EventoDto:
        evento_dto = EventoDto()
        evento_dto.tipo = entity.tipo
        evento_dto.fecha = entity.fecha
        evento_dto.lugar = entity.lugar
        evento_dto.distancia = entity.distancia
        evento_dto.nivel = entity.nivel
        evento_dto.id = entity.id
        evento_dto.nombre = entity.nombre

        return evento_dto
