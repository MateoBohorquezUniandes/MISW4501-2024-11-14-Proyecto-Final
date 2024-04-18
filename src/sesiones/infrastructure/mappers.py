from uuid import UUID
from sesiones.domain.entities import SesionDeportiva
from sesiones.domain.value_objects import Objetivo
from sesiones.infrastructure.dtos import SesionDeportiva as SesionDeportivaDTO


class SesionDeportivaMapper:
    def type(self) -> type:
        return SesionDeportiva

    def entity_to_dto(self, entity: SesionDeportiva) -> SesionDeportivaDTO:
        sesion_dto = SesionDeportivaDTO()
        sesion_dto.id = str(entity.id)
        sesion_dto.tipo_identificacion = entity.tipo_identificacion
        sesion_dto.identificacion = entity.identificacion
        sesion_dto.exigencia = entity.objetivo.exigencia
        sesion_dto.deporte = entity.objetivo.deporte
        sesion_dto.completedAt = entity.completed_at

        return sesion_dto

    def dto_to_entity(self, dto: SesionDeportivaDTO) -> SesionDeportiva:
        objetivo = Objetivo(dto.exigencia, dto.deporte)
        return SesionDeportiva(
            UUID(dto.id),
            dto.createdAt,
            dto.updateAt,
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
            objetivo=objetivo,
            completed_at=dto.completedAt,
        )
