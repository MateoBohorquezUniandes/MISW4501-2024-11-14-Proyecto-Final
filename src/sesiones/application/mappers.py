from dataclasses import asdict
from uuid import UUID
from seedwork.application.dtos import Mapper as ApplicationMapper
from seedwork.domain.repositories import Mapper as DomainMapper
from sesiones.application.dtos import SesionDeportivaDTO, ObjetivoDTO
from sesiones.domain.entities import SesionDeportiva
from sesiones.domain.value_objects import Objetivo


# #####################################################################################
# Application Mappers
# #####################################################################################


class SesionDeportivaDTODictMapper(ApplicationMapper):
    def _external_to_objetivo_dto(self, external: dict) -> ObjetivoDTO:
        return ObjetivoDTO(
            external.get("exigencia", ""),
            external.get("deporte", ""),
        )

    def external_to_dto(self, external: dict) -> SesionDeportivaDTO:
        objetivo = self._external_to_objetivo_dto(external.get("objetivo", {}))
        return SesionDeportivaDTO(
            id=external.get("id", ""),
            tipo_identificacion=external.get("tipo_identificacion", ""),
            identificacion=external.get("identificacion", ""),
            objetivo=objetivo,
        )

    def dto_to_external(self, dto: SesionDeportivaDTO) -> dict:
        return asdict(dto)


# #####################################################################################
# Domain Mappers
# #####################################################################################


class SesionDeportivaDTOEntityMapper(DomainMapper):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def type(self) -> type:
        return SesionDeportiva

    def dto_to_entity(self, dto: SesionDeportivaDTO) -> SesionDeportiva:
        objetivo = Objetivo(dto.objetivo.exigencia, dto.objetivo.deporte)
        args = [UUID(dto.id)] if dto.id else []

        sesion = SesionDeportiva(
            *args,
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
            objetivo=objetivo
        )
        return sesion

    def entity_to_dto(self, entity: SesionDeportiva) -> SesionDeportivaDTO:
        objetivo = ObjetivoDTO(entity.objetivo.exigencia, entity.objetivo.deporte)
        completed_at = entity.completed_at.strftime(self.DATE_FORMAT) if entity.completed_at else ""

        return SesionDeportivaDTO(
            str(entity.id),
            entity.created_at.strftime(self.DATE_FORMAT),
            entity.updated_at.strftime(self.DATE_FORMAT),
            entity.tipo_identificacion,
            entity.identificacion,
            completed_at,
            objetivo=objetivo,
        )
