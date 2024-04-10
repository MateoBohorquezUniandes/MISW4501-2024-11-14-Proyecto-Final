from perfiles.application.dtos import (
    ClasificacionRiesgoDTO,
    IndiceMasaCorporalDTO,
    InformacionDemograficaDTO,
    InformacionFisiologicaDTO,
    PerfilDemograficoDTO,
    ReporteSanguineoDTO,
    ResultadoElementoSanguineoDTO,
)
from perfiles.domain.entities import (
    PerfilAlimenticio,
    PerfilDemografico,
    PerfilDeportivo,
    ReporteSanguineo,
)
from perfiles.domain.value_objects import (
    ClasificacionRiesgo,
    InformacionDemografica,
    InformacionFisiologica,
    ResultadoElementoSanguineo,
)
from seedwork.application.dtos import Mapper as ApplicationMapper
from seedwork.domain.entities import Entity
from seedwork.domain.repositories import Mapper as DomainMapper
from seedwork.domain.repositories import (
    UnidirectionalMapper as UnidirectionalDomainMapper,
)

# #####################################################################################
# Application Mappers
# #####################################################################################


class PerfilDemograficoJsonDtoMapper(ApplicationMapper):

    def _external_to_demografia_dto(self, external: dict) -> InformacionDemograficaDTO:
        return InformacionDemograficaDTO(
            external.get("pais_residencia"),
            external.get("ciudad_residencia"),
        )

    def _external_to_fisiolofia_dto(self, external: dict) -> InformacionFisiologicaDTO:
        return InformacionFisiologicaDTO(
            external.get("genero"),
            int(external.get("edad")),
            float(external.get("altura")),
            float(external.get("peso")),
        )

    def _external_to_reportes_sanguineo_dto(
        self, external: list[dict]
    ) -> ReporteSanguineoDTO:
        reportes: list[ReporteSanguineoDTO] = []
        for reporte in external:
            reportes.append(
                ReporteSanguineoDTO(
                    ResultadoElementoSanguineoDTO(
                        tipo_examen=reporte.get("tipo_examen"),
                        valor=float(reporte.get("valor")),
                        unidad=reporte.get("unidad"),
                    )
                )
            )
        return reportes

    def external_to_dto(self, external: any) -> PerfilDemograficoDTO:
        demografia = self._external_to_demografia_dto(external.get("demografia"))
        fisiologia = self._external_to_fisiolofia_dto(external.get("fisiologia"))
        reportes = self._external_to_reportes_sanguineo_dto(
            external.get("reportes_sanguineo", [])
        )
        deportes = external.get("deportes", [])
        return PerfilDemograficoDTO(
            tipo_identificacion=external.get("tipo_identificacion"),
            identificacion=external.get("identificacion"),
            reportes_sanguineo=reportes,
            demografia=demografia,
            fisiologia=fisiologia,
            deportes=deportes,
        )

    def dto_to_external(self, dto: PerfilDemograficoDTO) -> any:
        return dto.__dict__


# #####################################################################################
# Domain Mappers
# #####################################################################################


class PerfilDemograficoDTOEntityMapper(DomainMapper):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def type(self) -> type:
        return PerfilDemografico

    def _dto_to_reportes_sanguineo(
        self, dtos: list[ReporteSanguineoDTO]
    ) -> list[ReporteSanguineo]:
        reportes: list[ReporteSanguineo] = []
        for reporte in dtos:
            reportes.append(
                ReporteSanguineo(
                    ResultadoElementoSanguineo(
                        tipo_examen=reporte.resultado.tipo_examen,
                        valor=reporte.resultado.valor,
                        unidad=reporte.resultado.unidad,
                    )
                )
            )
        return reportes

    def dto_to_entity(self, dto: PerfilDemograficoDTO) -> PerfilDemografico:
        demografia = InformacionDemografica(dto.demografia.pais, dto.demografia.ciudad)
        fisiologia = InformacionFisiologica(
            dto.fisiologia.genero,
            dto.fisiologia.edad,
            dto.fisiologia.altura,
            dto.fisiologia.peso,
        )
        clasificacion = ClasificacionRiesgo(fisiologia.calculate_imc())
        reportes = self._dto_to_reportes_sanguineo(dto.reportes_sanguineo)
        return PerfilDemografico(
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
            clasificacion_riesgo=clasificacion,
            reportes_sanguineo=reportes,
            demografia=demografia,
            fisiologia=fisiologia,
        )

    def _entity_to_reportes_sanguineo_dto(
        self, entities: list[ReporteSanguineo]
    ) -> list[ReporteSanguineoDTO]:
        reportes: list[ReporteSanguineo] = []
        for reporte in entities:
            reportes.append(
                ReporteSanguineoDTO(
                    ResultadoElementoSanguineoDTO(
                        tipo_examen=reporte.resultado.tipo_examen,
                        valor=reporte.resultado.valor,
                        unidad=reporte.resultado.unidad,
                    )
                )
            )
        return reportes

    def entity_to_dto(self, entity: PerfilDemografico) -> PerfilDemograficoDTO:
        demografia = InformacionDemografica(
            entity.demografia.pais, entity.demografia.ciudad
        )
        fisiologia = InformacionFisiologica(
            entity.fisiologia.genero,
            entity.fisiologia.edad,
            entity.fisiologia.altura,
            entity.fisiologia.peso,
        )
        clasificacion = ClasificacionRiesgoDTO(
            IndiceMasaCorporalDTO(
                entity.clasificacion_riesgo.imc.valor,
                entity.clasificacion_riesgo.imc.categoria,
            ),
            entity.clasificacion_riesgo.riesgo,
        )
        reportes = self._entity_to_reportes_sanguineo_dto(entity.reportes_sanguineo)
        return PerfilDemograficoDTO(
            tipo_identificacion=entity.tipo_identificacion,
            identificacion=entity.identificacion,
            clasificacion_riesgo=clasificacion,
            reportes_sanguineo=reportes,
            demografia=demografia,
            fisiologia=fisiologia,
        )


class PerfilDeportivoInitialEntityMapper(UnidirectionalDomainMapper):
    def type(self) -> type:
        return PerfilDeportivo

    def map(self, dto: PerfilDemograficoDTO) -> PerfilDeportivo:
        return PerfilDeportivo(
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
        )


class PerfilAlimenticioInitialEntityMapper(UnidirectionalDomainMapper):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def type(self) -> type:
        return PerfilAlimenticio

    def map(self, dto: PerfilDemograficoDTO) -> PerfilAlimenticio:
        return PerfilAlimenticio(
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
        )
