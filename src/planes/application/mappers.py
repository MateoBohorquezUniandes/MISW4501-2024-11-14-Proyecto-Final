from dataclasses import asdict
from uuid import UUID

from planes.application.dtos import (
    DuracionDTO,
    EntrenamientoDTO,
    FrecuenciaDTO,
    GrupoAlimenticioDTO,
    ObjetivoEntrenamientoDTO,
    PlanEntrenamientoDTO,
    RutinaAlimentacionDTO,
    RutinaRecuperacionDTO,
    UsuarioPlanDTO,
)
from planes.domain.entities import (
    Entrenamiento,
    GrupoAlimenticio,
    PlanEntrenamiento,
    RutinaAlimentacion,
    RutinaRecuperacion,
    UsuarioPlan,
)
from planes.domain.value_objects import (
    EXIGENCIA,
    Duracion,
    Frecuencia,
    Imagen,
    ObjetivoEntrenamiento,
)
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
        return asdict(dto)


class ObjetivoEntrenamientoDTODictMapper(ApplicationMapper):
    def type(self) -> type:
        return ObjetivoEntrenamiento

    def external_to_dto(self, external: dict) -> ObjetivoEntrenamientoDTO:
        return ObjetivoEntrenamientoDTO(
            external.get("exigencia", ""),
            external.get("deporte", ""),
        )

    def dto_to_external(self, dto: ObjetivoEntrenamientoDTO) -> dict:
        return asdict(dto)


class PlanEntrenamientoDTODictMapper(ApplicationMapper):
    def _external_to_objetivo_dto(self, external: dict) -> ObjetivoEntrenamientoDTO:
        return ObjetivoEntrenamientoDTO(
            external.get("exigencia", ""),
            external.get("deporte", ""),
        )

    def external_to_dto(self, external: dict) -> PlanEntrenamientoDTO:
        objetivo = ObjetivoEntrenamientoDTODictMapper().external_to_dto(
            external.get("objetivo", {})
        )
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
        return asdict(dto)


class UsuarioPlanDTODictMapper(ApplicationMapper):
    def external_to_dto(self, external: dict) -> UsuarioPlanDTO:
        return UsuarioPlanDTO(
            tipo_identificacion=external.get("tipo_identificacion", ""),
            identificacion=external.get("identificacion", ""),
            deportes=external.get("deportes", ""),
        )

    def dto_to_external(self, dto: PlanEntrenamientoDTO) -> dict:
        return asdict(dto)


class GrupoAlimenticioDTODictMapper(ApplicationMapper):
    def external_to_dto(self, external: dict) -> GrupoAlimenticioDTO:
        return GrupoAlimenticioDTO(
            id=external.get("", ""),
            grupo=external.get("grupo", ""),
            porcion=float(external.get("porcion", "")),
            unidad=external.get("unidad", ""),
            calorias=float(external.get("calorias", "")),
        )

    def dto_to_external(self, dto: GrupoAlimenticioDTO) -> dict:
        return asdict(dto)


class RutinaAlimentacionDTODictMapper(ApplicationMapper):
    def external_to_dto(self, external: dict) -> RutinaAlimentacionDTO:
        mapper = GrupoAlimenticioDTODictMapper()
        grupos = [
            mapper.external_to_dto(g) for g in external.get("grupos_alimenticios", [])
        ]
        return RutinaAlimentacionDTO(
            id=external.get("", ""),
            nombre=external.get("nombre", ""),
            descripcion=external.get("descripcion", ""),
            imagen=external.get("imagen", ""),
            tipo_alimentacion=external.get("tipo_alimentacion", ""),
            deporte=external.get("deporte", ""),
            grupos_alimenticios=grupos,
        )

    def dto_to_external(self, dto: RutinaAlimentacionDTO) -> dict:
        return asdict(dto)


class RutinaRecuperacionDTODictMapper(ApplicationMapper):
    def _external_to_frecuencia_dto(self, external: dict) -> DuracionDTO:
        return FrecuenciaDTO(
            int(external.get("valor", "0")),
            external.get("unidad", ""),
        )

    def external_to_dto(self, external: dict) -> RutinaRecuperacionDTO:
        frecuencia = self._external_to_frecuencia_dto(external.get("frecuencia", {}))
        return RutinaRecuperacionDTO(
            id=external.get("", ""),
            nombre=external.get("nombre", ""),
            descripcion=external.get("descripcion", ""),
            imagen=external.get("imagen", ""),
            deporte=external.get("deporte", ""),
            frecuencia=frecuencia,
        )

    def dto_to_external(self, dto: RutinaRecuperacionDTO) -> dict:
        return asdict(dto)


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


class ObjetivoEntrenamientoDTOEntityMapper(DomainMapper):
    def type(self) -> type:
        return ObjetivoEntrenamiento

    def dto_to_entity(self, dto: ObjetivoEntrenamientoDTO) -> ObjetivoEntrenamiento:
        return ObjetivoEntrenamiento(EXIGENCIA.get(dto.exigencia), dto.deporte)

    def entity_to_dto(self, vo: ObjetivoEntrenamiento) -> ObjetivoEntrenamientoDTO:
        return ObjetivoEntrenamientoDTO(vo.exigencia, vo.deporte)


class PlanEntrenamientoDTOEntityMapper(DomainMapper):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def type(self) -> type:
        return PlanEntrenamiento

    def dto_to_entity(self, dto: PlanEntrenamientoDTO) -> PlanEntrenamiento:
        objetivo = ObjetivoEntrenamientoDTOEntityMapper().dto_to_entity(dto.objetivo)
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
        objetivo = ObjetivoEntrenamientoDTOEntityMapper().entity_to_dto(entity.objetivo)
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
            entity.created_at.strftime(self.DATE_FORMAT),
            entity.updated_at.strftime(self.DATE_FORMAT),
            entity.tipo_identificacion,
            entity.identificacion,
            planes_entrenamiento=planes,
        )


class GrupoAlimenticioDTOEntityMapper(DomainMapper):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def type(self) -> type:
        return GrupoAlimenticio

    def dto_to_entity(self, dto: GrupoAlimenticioDTO) -> GrupoAlimenticio:
        args = [UUID(dto.id)] if dto.id else []
        return GrupoAlimenticio(
            *args,
            grupo=dto.grupo,
            porcion=dto.porcion,
            unidad=dto.unidad,
            calorias=dto.calorias,
        )

    def entity_to_dto(self, entity: GrupoAlimenticio) -> GrupoAlimenticioDTO:
        return GrupoAlimenticioDTO(
            entity.created_at.strftime(self.DATE_FORMAT),
            entity.updated_at.strftime(self.DATE_FORMAT),
            entity.id,
            grupo=entity.grupo,
            porcion=entity.porcion,
            unidad=entity.unidad,
            calorias=entity.calorias,
        )


class RutinaAlimentacionDTOEntityMapper(DomainMapper):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def type(self) -> type:
        return RutinaAlimentacion

    def dto_to_entity(self, dto: RutinaAlimentacionDTO) -> RutinaAlimentacion:
        args = [UUID(dto.id)] if dto.id else []
        mapper = GrupoAlimenticioDTOEntityMapper()
        grupos = [mapper.dto_to_entity(g) for g in dto.grupos_alimenticios]
        return RutinaAlimentacion(
            *args,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            imagen=dto.imagen,
            tipo_alimentacion=dto.tipo_alimentacion,
            grupos_alimenticios=grupos,
            deporte=dto.deporte,
        )

    def entity_to_dto(self, entity: RutinaAlimentacion) -> RutinaAlimentacionDTO:
        mapper = GrupoAlimenticioDTOEntityMapper()
        grupos = [mapper.entity_to_dto(g) for g in entity.grupos_alimenticios]
        return RutinaAlimentacionDTO(
            entity.created_at.strftime(self.DATE_FORMAT),
            entity.updated_at.strftime(self.DATE_FORMAT),
            entity.id,
            nombre=entity.nombre,
            descripcion=entity.descripcion,
            imagen=entity.imagen,
            tipo_alimentacion=entity.tipo_alimentacion,
            grupos_alimenticios=grupos,
        )


class RutinaRecuperacionDTOEntityMapper(DomainMapper):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def type(self) -> type:
        return RutinaRecuperacion

    def dto_to_entity(self, dto: RutinaRecuperacionDTO) -> RutinaRecuperacion:
        args = [UUID(dto.id)] if dto.id else []
        frecuencia = Frecuencia(dto.frecuencia.valor, dto.frecuencia.unidad)
        return RutinaRecuperacion(
            *args,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            imagen=dto.imagen,
            deporte=dto.deporte,
            frecuencia=frecuencia,
        )

    def entity_to_dto(self, entity: RutinaRecuperacion) -> RutinaRecuperacionDTO:
        frecuencia = FrecuenciaDTO(entity.frecuencia.valor, entity.frecuencia.unidad)
        return RutinaRecuperacionDTO(
            entity.created_at.strftime(self.DATE_FORMAT),
            entity.updated_at.strftime(self.DATE_FORMAT),
            entity.id,
            nombre=entity.nombre,
            descripcion=entity.descripcion,
            imagen=entity.imagen,
            deporte=entity.deporte,
            frecuencia=frecuencia,
        )
