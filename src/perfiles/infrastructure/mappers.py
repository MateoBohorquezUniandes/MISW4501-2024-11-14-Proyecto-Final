from uuid import UUID
from perfiles.domain.entities import (
    Alimento,
    HabitoDeportivo,
    PerfilAlimenticio,
    PerfilDemografico,
    PerfilDeportivo,
    ReporteSanguineo,
    Molestia,
)
from perfiles.domain.value_objects import (
    AlimentoAsociado,
    ClasificacionRiesgo,
    HabitoDeportivoFrecuencia,
    IndiceMasaCorporal,
    InformacionDemografica,
    InformacionFisiologica,
    ResultadoElementoSanguineo,
    MolestiaTipo,
    VolumenMaximoOxigeno,
)
from perfiles.infrastructure.dtos import HabitoDeportivo as HabitoDeportivoDTO
from perfiles.infrastructure.dtos import PerfilAlimenticio as PerfilAlimenticioDTO
from perfiles.infrastructure.dtos import PerfilDemografico as PerfilDemograficoDTO
from perfiles.infrastructure.dtos import PerfilDeportivo as PerfilDeportivoDTO
from perfiles.infrastructure.dtos import Molestia as MolestiaDTO
from perfiles.infrastructure.dtos import Alimento as AlimentoDTO
from perfiles.infrastructure.dtos import AlimentoAsociado as AlimentoAsociadoDTO
from seedwork.domain.repositories import Mapper


class PerfilDemograficoMapper(Mapper):
    def type(self) -> type:
        return PerfilDemografico

    def entity_to_dto(
        self, entity: PerfilDemografico, perfil_dto: PerfilDemograficoDTO = None
    ) -> PerfilDemograficoDTO:
        perfil_dto = perfil_dto or PerfilDemograficoDTO()
        perfil_dto.tipo_identificacion = entity.tipo_identificacion
        perfil_dto.identificacion = entity.identificacion

        perfil_dto.genero = entity.fisiologia.genero
        perfil_dto.edad = entity.fisiologia.edad
        perfil_dto.peso = entity.fisiologia.peso
        perfil_dto.altura = entity.fisiologia.altura
        perfil_dto.pais = entity.demografia.pais
        perfil_dto.ciudad = entity.demografia.ciudad

        perfil_dto.imc_valor = entity.clasificacion_riesgo.imc.valor
        perfil_dto.imc_cateroria = entity.clasificacion_riesgo.imc.categoria
        perfil_dto.vo_max_valor = entity.clasificacion_riesgo.vo_max.valor
        perfil_dto.vo_max_cateroria = entity.clasificacion_riesgo.vo_max.categoria
        perfil_dto.clasificacion_riesgo = entity.clasificacion_riesgo.riesgo

        return perfil_dto

    def dto_to_entity(self, dto: PerfilDemograficoDTO) -> PerfilDemografico:
        clasificacion_riesgo = ClasificacionRiesgo(
            imc=IndiceMasaCorporal(dto.imc_valor, dto.imc_cateroria),
            vo_max=VolumenMaximoOxigeno(dto.vo_max_valor, dto.vo_max_cateroria),
        )

        reportes = list()
        for reporte_dto in dto.reportes_sanguineos:
            reportes.append(
                ReporteSanguineo(
                    resultado=ResultadoElementoSanguineo(
                        tipo_examen=reporte_dto.tipo_examen,
                        valor=reporte_dto.valor,
                        unidad=reporte_dto.unidad,
                    )
                )
            )

        demografia = InformacionDemografica(dto.pais, dto.ciudad)
        fisiologia = InformacionFisiologica(dto.genero, dto.edad, dto.altura, dto.peso)
        return PerfilDemografico(
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
            clasificacion_riesgo=clasificacion_riesgo,
            reportes_sanguineo=reportes,
            demografia=demografia,
            fisiologia=fisiologia,
        )


class HabitoDeportivoMapper(Mapper):
    def type(self) -> type:
        return HabitoDeportivo

    def dto_to_entity(self, dto: HabitoDeportivoDTO) -> HabitoDeportivo:
        return HabitoDeportivo(
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
            descripcion=dto.descripcion,
            frecuencia=HabitoDeportivoFrecuencia(dto.frecuencia),
            titulo=dto.titulo,
        )

    def entity_to_dto(self, entity: HabitoDeportivo) -> HabitoDeportivoDTO:
        habito_dto = HabitoDeportivoDTO()
        habito_dto.frecuencia = entity.frecuencia
        habito_dto.descripcion = entity.descripcion
        habito_dto.titulo = entity.titulo
        habito_dto.tipo_identificacion = entity.tipo_identificacion
        habito_dto.identificacion = entity.identificacion

        return habito_dto


class MolestiaMapper(Mapper):
    def type(self) -> type:
        return Molestia

    def dto_to_entity(self, dto: MolestiaDTO) -> Molestia:
        return Molestia(
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
            descripcion=dto.descripcion,
            tipo=MolestiaTipo(dto.tipo),
            titulo=dto.titulo,
            fecha=dto.fecha,
        )

    def entity_to_dto(self, entity: Molestia) -> MolestiaDTO:
        molestia_dto = MolestiaDTO()
        molestia_dto.tipo = entity.tipo
        molestia_dto.descripcion = entity.descripcion
        molestia_dto.titulo = entity.titulo
        molestia_dto.tipo_identificacion = entity.tipo_identificacion
        molestia_dto.identificacion = entity.identificacion
        molestia_dto.fecha = entity.fecha

        return molestia_dto


class PerfilDeportivoMapper(Mapper):
    def type(self) -> type:
        return PerfilDeportivo

    def entity_to_dto(self, entity: PerfilDeportivo) -> PerfilDeportivoDTO:
        mapper = HabitoDeportivoMapper()
        habitos_deportivos = [
            mapper.entity_to_dto(h) for h in entity.habitos_deportivos
        ]
        molestias = [mapper.entity_to_dto(h) for h in entity.molestias]
        perfil = PerfilDeportivoDTO()
        perfil.tipo_identificacion = entity.tipo_identificacion
        perfil.identificacion = entity.identificacion
        perfil.habitos_deportivos = habitos_deportivos
        perfil.molestias = molestias
        return perfil

    def dto_to_entity(self, dto: PerfilDeportivoDTO) -> PerfilDeportivo:
        mapper = HabitoDeportivoMapper()
        habitos_deportivos = [mapper.dto_to_entity(h) for h in dto.habitos_deportivos]
        mapper_molestia = MolestiaMapper()
        molestias = [mapper_molestia.dto_to_entity(h) for h in dto.molestias]
        return PerfilDeportivo(
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
            habitos_deportivos=habitos_deportivos,
            molestias=molestias,
        )


class PerfilAlimenticioMapper(Mapper):
    def type(self) -> type:
        return PerfilAlimenticio

    def entity_to_dto(self, entity: PerfilAlimenticio) -> PerfilAlimenticioDTO:
        perfil = PerfilAlimenticioDTO()
        perfil.tipo_identificacion = entity.tipo_identificacion
        perfil.identificacion = entity.identificacion
        perfil.tipo_alimentacion = entity.tipo_alimentacion
        return perfil

    def dto_to_entity(self, dto: PerfilAlimenticioDTO) -> PerfilAlimenticio:
        return PerfilAlimenticio(
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
            tipo_alimentacion=dto.tipo_alimentacion
        )


class AlimentoMapper(Mapper):
    def type(self) -> type:
        return Alimento

    def entity_to_dto(self, entity: Alimento) -> AlimentoDTO:
        alimento = AlimentoDTO()
        alimento.id = str(entity.id)
        alimento.nombre = entity.nombre
        alimento.categoria = entity.categoria
        return alimento

    def dto_to_entity(self, dto: AlimentoDTO) -> Alimento:
        return Alimento(
            UUID(dto.id),
            dto.createdAt,
            dto.updateAt,
            dto.nombre,
            dto.categoria,
        )


class AlimentoAsociadoMapper(Mapper):
    def type(self) -> type:
        return AlimentoAsociado

    def entity_to_dto(self, entity: AlimentoAsociado) -> AlimentoAsociadoDTO:
        asociacion = AlimentoAsociadoDTO()
        asociacion.id_alimento = entity.id_alimento
        asociacion.tipo_identificacion = entity.tipo_identificacion
        asociacion.identificacion = entity.identificacion
        asociacion.tipo = entity.tipo
        return asociacion

    def dto_to_entity(self, dto: AlimentoAsociadoDTO) -> AlimentoAsociado:
        return AlimentoAsociado(
            dto.id_alimento,
            dto.tipo_identificacion,
            dto.identificacion,
            dto.tipo,
        )
