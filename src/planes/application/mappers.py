from uuid import UUID

from planes.application.dtos import (
    DuracionDTO,
    EntrenamientoDTO,
    ObjetivoEntrenamientoDTO,
    PlanEntrenamientoDTO,
    UsuarioPlanDTO,
)
from planes.domain.entities import Entrenamiento, PlanEntrenamiento, UsuarioPlan
from planes.domain.value_objects import Duracion, Imagen, ObjetivoEntrenamiento
from seedwork.application.dtos import Mapper as ApplicationMapper
from seedwork.domain.repositories import Mapper as DomainMapper

# #####################################################################################
# Application Mappers
# #####################################################################################


class EntrenamientoDTODictMapper(ApplicationMapper):
    def _external_to_duracion_dto(self, external: dict) -> DuracionDTO:
        return DuracionDTO(
            int(external.get("valor", "0")),
            external.get("unidad", ""),
            int(external.get("series", "0")),
        )

    def external_to_dto(self, external: dict) -> EntrenamientoDTO:
        duracion = self._external_to_duracion_dto(external.get("duracion", {}))
        return EntrenamientoDTO(
            id=external.get("id", ""),
            nombre=external.get("nombre", ""),
            descripcion=external.get("descripcion", ""),
            grupo_muscular=external.get("grupo_muscular", ""),
            imagen=external.get("imagen", ""),
            duracion=duracion,
        )

    def dto_to_external(self, dto: EntrenamientoDTO) -> dict:
        return dto.__dict__


class PlanEntrenamientoDTODictMapper(ApplicationMapper):
    def _external_to_objetivo_dto(self, external: dict) -> ObjetivoEntrenamientoDTO:
        return ObjetivoEntrenamientoDTO(
            external.get("exigencia", ""),
            external.get("deporte", ""),
        )

    def external_to_dto(self, external: dict) -> PlanEntrenamientoDTO:
        objetivo = self._external_to_objetivo_dto(external.get("objetivo", {}))
        mapper = EntrenamientoDTODictMapper()
        entrenamientos = [
            mapper.external_to_dto(e) for e in external.get("entrenamientos", [])
        ]
        return PlanEntrenamientoDTO(
            id=external.get("id", ""),
            nombre=external.get("nombre", ""),
            categoria=external.get("categoria", ""),
            descripcion=external.get("descripcion", ""),
            objetivo=objetivo,
            entrenamientos=entrenamientos,
        )

    def dto_to_external(self, dto: PlanEntrenamientoDTO) -> dict:
        return dto.__dict__


class UsuarioPlanDTODictMapper(ApplicationMapper):
    def external_to_dto(self, external: dict) -> UsuarioPlanDTO:

        return UsuarioPlanDTO(
            tipo_identificacion=external.get("tipo_identificacion", ""),
            identificacion=external.get("identificacion", ""),
            deportes=external.get("deportes", ""),
        )

    def dto_to_external(self, dto: PlanEntrenamientoDTO) -> dict:
        return dto.__dict__


# #####################################################################################
# Domain Mappers
# #####################################################################################


class EntrenamientoDTOEntityMapper(DomainMapper):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def type(self) -> type:
        return Entrenamiento

    def dto_to_entity(self, dto: EntrenamientoDTO) -> Entrenamiento:
        duracion = Duracion(
            dto.duracion.valor,
            dto.duracion.unidad,
            dto.duracion.series,
        )
        args = [UUID(dto.id)] if dto.id else []
        entrenamiento = Entrenamiento(
            *args,
            nombre=dto.nombre,
            grupo_muscular=dto.grupo_muscular,
            descripcion=dto.descripcion,
            imagen=Imagen(dto.imagen),
            duracion=duracion,
        )
        return entrenamiento

    def entity_to_dto(self, entity: Entrenamiento) -> EntrenamientoDTO:
        duracion_dto = DuracionDTO(
            entity.duracion.valor,
            entity.duracion.unidad,
            entity.duracion.series,
        )
        return EntrenamientoDTO(
            entity.created_at.strftime(self.DATE_FORMAT),
            entity.updated_at.strftime(self.DATE_FORMAT),
            entity.id,
            entity.nombre,
            entity.descripcion,
            entity.grupo_muscular,
            entity.imagen.url,
            duracion_dto,
        )


class PlanEntrenamientoDTOEntityMapper(DomainMapper):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def type(self) -> type:
        return PlanEntrenamiento

    def dto_to_entity(self, dto: PlanEntrenamientoDTO) -> PlanEntrenamiento:
        objetivo = ObjetivoEntrenamiento(dto.objetivo.exigencia, dto.objetivo.deporte)
        mapper = EntrenamientoDTOEntityMapper()
        entrenamientos = [mapper.dto_to_entity(e) for e in dto.entrenamientos]

        args = [UUID(dto.id)] if dto.id else []
        plan = PlanEntrenamiento(
            *args,
            nombre=dto.nombre,
            categoria=dto.categoria,
            descripcion=dto.descripcion,
            objetivo=objetivo,
            entrenamientos=entrenamientos,
        )
        return plan

    def entity_to_dto(self, entity: PlanEntrenamiento) -> PlanEntrenamientoDTO:
        objetivo = ObjetivoEntrenamientoDTO(
            entity.objetivo.exigencia, entity.objetivo.deporte
        )
        mapper = EntrenamientoDTOEntityMapper()
        entrenamientos = [mapper.entity_to_dto(e) for e in entity.entrenamientos]

        return PlanEntrenamientoDTO(
            entity.created_at.strftime(self.DATE_FORMAT),
            entity.updated_at.strftime(self.DATE_FORMAT),
            entity.id,
            entity.nombre,
            entity.categoria,
            entity.descripcion,
            objetivo,
            entrenamientos,
        )


class UsuarioPlanDTOEntityMapper(DomainMapper):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def type(self) -> type:
        return UsuarioPlan

    def dto_to_entity(self, dto: UsuarioPlanDTO) -> UsuarioPlan:
        return UsuarioPlan(
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
        )

    def entity_to_dto(self, entity: UsuarioPlan) -> UsuarioPlanDTO:
        mapper = PlanEntrenamientoDTOEntityMapper()
        planes = [mapper.entity_to_dto(p) for p in entity.planes_entrenamiento]
        return UsuarioPlanDTO(
            entity.created_at,
            entity.updated_at,
            entity.tipo_identificacion,
            entity.identificacion,
            planes_entrenamiento=planes,
        )
