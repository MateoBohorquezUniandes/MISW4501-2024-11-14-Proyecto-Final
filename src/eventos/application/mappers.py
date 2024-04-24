from uuid import UUID

from eventos.application.dtos import EventoDTO
from eventos.domain.entities import Evento

from seedwork.application.dtos import Mapper as ApplicationMapper
from seedwork.domain.repositories import Mapper as DomainMapper


# #####################################################################################
# Application Mappers
# #####################################################################################


class EventoDTODictMapper(ApplicationMapper):
    def external_to_dto(self, external: dict) -> EventoDTO:

        return EventoDTO(
            tipo=external.get("tipo", ""),
            fecha=external.get("fecha", ""),
            lugar=external.get("lugar", ""),
            distancia=external.get("distancia", ""),
            nivel=external.get("nivel", ""),
        )

    def dto_to_external(self, dto: EventoDTO) -> dict:
        return dto.__dict__


# #####################################################################################
# Domain Mappers
# #####################################################################################


class EventoDTOEntityMapper(DomainMapper):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def type(self) -> type:
        return Evento

    def dto_to_entity(self, dto: EventoDTO) -> Evento:

        args = [UUID(dto.id)] if dto.id else []
        evento = Evento(
            *args,
            tipo=dto.tipo,
            fecha=dto.fecha,
            lugar=dto.lugar,
            distancia=dto.distancia,
            nivel=dto.nivel
        )
        return evento

    def entity_to_dto(self, entity: Evento) -> EventoDTO:

        return EventoDTO(
            entity.id,
            entity.tipo,
            entity.fecha,
            entity.lugar,
            entity.distancia,
            entity.nivel,
        )
