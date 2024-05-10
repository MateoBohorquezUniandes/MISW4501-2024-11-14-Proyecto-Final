from dataclasses import asdict
from uuid import UUID

from eventos.application.dtos import EventoDTO
from eventos.domain.entities import Evento
from eventos.domain.value_objects import EventoAsociado
from seedwork.application.dtos import Mapper as ApplicationMapper
from seedwork.domain.repositories import Mapper as DomainMapper
from seedwork.domain.repositories import (
    UnidirectionalMapper as UnidirectionalDomainMapper,
)

# #####################################################################################
# Application Mappers
# #####################################################################################


class EventoDTODictMapper(ApplicationMapper):
    def external_to_dto(self, external: dict) -> EventoDTO:

        return EventoDTO(
            id=external.get("id", ""),
            tipo=external.get("tipo", ""),
            fecha=external.get("fecha", ""),
            lugar=external.get("lugar", ""),
            distancia=external.get("distancia", ""),
            nivel=external.get("nivel", ""),
            nombre=external.get("nombre", ""),
        )

    def dto_to_external(self, dto: EventoDTO) -> dict:
        return asdict(dto)


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
            nivel=dto.nivel,
            nombre=dto.nombre
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
            entity.nombre,
        )


class EventoAsociadoDTOEntityMapper(UnidirectionalDomainMapper):
    def type(self) -> type:
        return EventoAsociado

    def map(
        self,
        dto: EventoDTO,
        tipo_identificacion: str = None,
        identificacion: str = None,
    ) -> EventoAsociado:
        return EventoAsociado(
            id=dto.id,
            tipo_identificacion=tipo_identificacion,
            identificacion=identificacion,
        )
