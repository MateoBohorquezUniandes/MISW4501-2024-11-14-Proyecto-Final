from uuid import UUID

from planes.domain.entities import (
    Entrenamiento,
    GrupoAlimenticio,
    PlanEntrenamiento,
    RutinaAlimentacion,
    UsuarioPlan,
)
from planes.domain.value_objects import Duracion, Imagen, ObjetivoEntrenamiento
from planes.infrastructure.dtos import Entrenamiento as EntrenamientoDTO
from planes.infrastructure.dtos import GrupoAlimenticio as GrupoAlimenticioDTO
from planes.infrastructure.dtos import PlanEntrenamiento as PlanEntrenamientoDTO
from planes.infrastructure.dtos import RutinaAlimentacion as RutinaAlimentacionDTO
from planes.infrastructure.dtos import UsuarioPlan as UsuarioPlanDTO
from seedwork.domain.repositories import Mapper


class EntrenamientoMapper(Mapper):
    def type(self) -> type:
        return Entrenamiento

    def entity_to_dto(self, entity: Entrenamiento) -> EntrenamientoDTO:
        entrenamiento_dto = EntrenamientoDTO()
        entrenamiento_dto.id = str(entity.id)
        entrenamiento_dto.nombre = entity.nombre
        entrenamiento_dto.grupo_muscular = entity.grupo_muscular
        entrenamiento_dto.descripcion = entity.descripcion
        entrenamiento_dto.imagen = entity.imagen.url
        entrenamiento_dto.duracion = entity.duracion.valor
        entrenamiento_dto.duracion_unidad = entity.duracion.unidad
        entrenamiento_dto.series = entity.duracion.series

        return entrenamiento_dto

    def dto_to_entity(self, dto: EntrenamientoDTO) -> Entrenamiento:
        duracion = Duracion(dto.duracion, dto.duracion_unidad, dto.series)
        imagen = Imagen(dto.imagen)
        return Entrenamiento(
            UUID(dto.id),
            dto.createdAt,
            dto.updateAt,
            nombre=dto.nombre,
            grupo_muscular=dto.grupo_muscular,
            descripcion=dto.descripcion,
            imagen=imagen,
            duracion=duracion,
        )


class PlanEntrenamientoMapper(Mapper):
    def type(self) -> type:
        return PlanEntrenamiento

    def entity_to_dto(self, entity: PlanEntrenamiento) -> PlanEntrenamientoDTO:
        plan_dto = PlanEntrenamientoDTO()
        plan_dto.id = str(entity.id)
        plan_dto.nombre = entity.nombre
        plan_dto.categoria = entity.categoria
        plan_dto.descripcion = entity.descripcion
        plan_dto.nivel_exigencia = entity.objetivo.exigencia
        plan_dto.deporte_objetivo = entity.objetivo.deporte

        return plan_dto

    def dto_to_entity(self, dto: PlanEntrenamientoDTO) -> PlanEntrenamiento:
        objetivo = ObjetivoEntrenamiento(dto.nivel_exigencia, dto.deporte_objetivo)
        mapper = EntrenamientoMapper()
        entrenamientos = [mapper.dto_to_entity(e) for e in dto.entrenamientos]
        return PlanEntrenamiento(
            UUID(dto.id),
            dto.createdAt,
            dto.updateAt,
            nombre=dto.nombre,
            categoria=dto.categoria,
            descripcion=dto.descripcion,
            objetivo=objetivo,
            entrenamientos=entrenamientos,
        )


class UsuarioPlanMapper(Mapper):
    def type(self) -> type:
        return UsuarioPlan

    def entity_to_dto(self, entity: UsuarioPlan) -> UsuarioPlanDTO:
        usuario_dto = UsuarioPlanDTO()
        usuario_dto.id = str(entity.id)
        usuario_dto.tipo_identificacion = entity.tipo_identificacion
        usuario_dto.identificacion = entity.identificacion

        return usuario_dto

    def dto_to_entity(self, dto: UsuarioPlanDTO) -> UsuarioPlan:
        mapper = PlanEntrenamientoMapper()
        planes = [mapper.dto_to_entity(p) for p in dto.planes]
        return UsuarioPlan(
            created_at=dto.createdAt,
            updated_at=dto.updateAt,
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
            planes_entrenamiento=planes,
        )


class GrupoAlimenticioMapper(Mapper):
    def type(self) -> type:
        return GrupoAlimenticio

    def entity_to_dto(self, entity: GrupoAlimenticio) -> GrupoAlimenticioDTO:
        grupo_dto = GrupoAlimenticioDTO()
        grupo_dto.id = str(entity.id)
        grupo_dto.grupo = entity.grupo
        grupo_dto.porcion = entity.porcion
        grupo_dto.porcion_unidad = entity.unidad
        grupo_dto.calorias = entity.calorias

        return grupo_dto

    def dto_to_entity(self, dto: GrupoAlimenticioDTO) -> GrupoAlimenticio:
        return GrupoAlimenticio(
            UUID(dto.id),
            created_at=dto.createdAt,
            updated_at=dto.updateAt,
            grupo=dto.grupo,
            porcion=dto.porcion,
            unidad=dto.porcion_unidad,
            calorias=dto.calorias,
        )


class RutinaAlimentacionMapper(Mapper):
    def type(self) -> type:
        return RutinaAlimentacion

    def entity_to_dto(self, entity: RutinaAlimentacion) -> RutinaAlimentacionDTO:
        rutina_dto = RutinaAlimentacionDTO()
        rutina_dto.id = str(entity.id)
        rutina_dto.nombre = entity.nombre
        rutina_dto.descripcion = entity.descripcion
        rutina_dto.imagen = entity.imagen
        rutina_dto.tipo_alimentacion = entity.tipo_alimentacion
        rutina_dto.deporte = entity.deporte

        return rutina_dto

    def dto_to_entity(self, dto: RutinaAlimentacionDTO) -> RutinaAlimentacion:
        mapper = GrupoAlimenticioMapper()
        grupos = [mapper.dto_to_entity(g) for g in dto.grupos_alimenticios]
        return RutinaAlimentacion(
            UUID(dto.id),
            created_at=dto.createdAt,
            updated_at=dto.updateAt,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            imagen=dto.imagen,
            tipo_alimentacion=dto.tipo_alimentacion,
            deporte=dto.deporte,
            grupos_alimenticios=grupos,
        )
