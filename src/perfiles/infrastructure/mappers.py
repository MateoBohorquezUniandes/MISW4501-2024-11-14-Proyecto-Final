from perfiles.domain.entities import (
    PerfilAlimenticio,
    PerfilDemografico,
    PerfilDeportivo,
    ReporteSanguineo,
    HabitoDeportivo
)
from perfiles.domain.value_objects import (
    ClasificacionRiesgo,
    IndiceMasaCorporal,
    InformacionDemografica,
    InformacionFisiologica,
    ResultadoElementoSanguineo,
    HabitoDeportivoFrecuencia,
)
from perfiles.infrastructure.dtos import PerfilDemografico as PerfilDemograficoDTO
from perfiles.infrastructure.dtos import ReporteSanguineo as ReporteSanguineoDTO
from perfiles.infrastructure.dtos import PerfilDeportivo as PerfilDeportivoDTO
from perfiles.infrastructure.dtos import PerfilAlimenticio as PerfilAlimenticioDTO
from perfiles.infrastructure.dtos import HabitoDeportivo as HabitoDeportivoDTO
from seedwork.domain.entities import Entity
from seedwork.domain.repositories import Mapper


class PerfilDemograficoMapper(Mapper):
    def type(self) -> type:
        return PerfilDemografico

    def entity_to_dto(self, entity: PerfilDemografico) -> PerfilDemograficoDTO:
        deportista_dto = PerfilDemograficoDTO()
        deportista_dto.tipo_identificacion = entity.tipo_identificacion
        deportista_dto.identificacion = entity.identificacion

        deportista_dto.genero = entity.fisiologia.genero
        deportista_dto.edad = entity.fisiologia.edad
        deportista_dto.peso = entity.fisiologia.peso
        deportista_dto.altura = entity.fisiologia.altura
        deportista_dto.pais = entity.demografia.pais
        deportista_dto.ciudad = entity.demografia.ciudad

        deportista_dto.imc_valor = entity.clasificacion_riesgo.imc.valor
        deportista_dto.imc_cateroria = entity.clasificacion_riesgo.imc.categoria
        deportista_dto.clasificacion_riesgo = entity.clasificacion_riesgo.riesgo

        reportes = list()
        for reporte in entity.reportes_sanguineo:
            reporte_dto = ReporteSanguineoDTO()
            reporte_dto.tipo_identificacion = entity.tipo_identificacion
            reporte_dto.identificacion = entity.identificacion

            reporte_dto.tipo_examen = reporte.resultado.tipo_examen
            reporte_dto.valor = reporte.resultado.valor
            reporte_dto.unidad = reporte.resultado.unidad
            reportes.append(reporte_dto)
        deportista_dto.reportes_sanguineos = reportes

        return deportista_dto

    def dto_to_entity(self, dto: PerfilDemograficoDTO) -> PerfilDemografico:
        clasificacion_riesgo = ClasificacionRiesgo(
            imc=IndiceMasaCorporal(dto.imc_valor, dto.imc_cateroria),
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


class PerfilDeportivoMapper(Mapper):
    def type(self) -> type:
        return PerfilDeportivo

    def entity_to_dto(self, entity: PerfilDeportivo) -> PerfilDeportivoDTO:
        perfil = PerfilDeportivoDTO()
        perfil.tipo_identificacion = entity.tipo_identificacion
        perfil.identificacion = entity.identificacion
        perfil.habitos_deportivos = entity.habitos_deportivos
        return perfil

    def dto_to_entity(self, dto: PerfilDeportivoDTO) -> PerfilDeportivo:
        return PerfilDeportivo(
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
            habitos_deportivos= dto.habitos_deportivos
        )


class PerfilAlimenticioMapper(Mapper):
    def type(self) -> type:
        return PerfilAlimenticio

    def entity_to_dto(self, entity: PerfilAlimenticio) -> PerfilAlimenticioDTO:
        perfil = PerfilAlimenticioDTO()
        perfil.tipo_identificacion = entity.tipo_identificacion
        perfil.identificacion = entity.identificacion
        return perfil

    def dto_to_entity(self, dto: PerfilAlimenticioDTO) -> PerfilAlimenticio:
        return PerfilAlimenticio(
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
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
            titulo=dto.titulo
        )
    def entity_to_dto(self, entity: HabitoDeportivo) -> HabitoDeportivoDTO:
        habito_dto = HabitoDeportivoDTO()
        habito_dto.frecuencia = entity.frecuencia
        habito_dto.descripcion = entity.descripcion
        habito_dto.titulo = entity.titulo
        habito_dto.tipo_identificacion = entity.tipo_identificacion
        habito_dto.identificacion = entity.identificacion 

        return habito_dto
    