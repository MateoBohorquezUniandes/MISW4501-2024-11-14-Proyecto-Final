from dataclasses import asdict
from uuid import UUID
from perfiles.application.dtos import (
    AlimentoDTO,
    ClasificacionRiesgoDTO,
    HabitoDeportivoDTO,
    IndiceMasaCorporalDTO,
    InformacionDemograficaDTO,
    InformacionFisiologicaDTO,
    PerfilAlimenticioDTO,
    PerfilDemograficoDTO,
    PerfilDeportivoDTO,
    ReporteSanguineoDTO,
    ResultadoElementoSanguineoDTO,
    MolestiaDTO,
    VolumenMaximoOxigenoDTO,
)
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
    CategoriaVOM,
    ClasificacionRiesgo,
    InformacionDemografica,
    InformacionFisiologica,
    ResultadoElementoSanguineo,
    VolumenMaximoOxigeno,
)
from seedwork.application.dtos import DTO, Mapper as ApplicationMapper
from seedwork.domain.entities import Entity
from seedwork.domain.repositories import Mapper as DomainMapper
from seedwork.domain.repositories import (
    UnidirectionalMapper as UnidirectionalDomainMapper,
)

# #####################################################################################
# Application Mappers
# #####################################################################################


class PerfilamientoInicialDTODictMapper(ApplicationMapper):

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

    def external_to_dto(self, external: any) -> PerfilDemograficoDTO:
        demografia = self._external_to_demografia_dto(external.get("demografia"))
        fisiologia = self._external_to_fisiolofia_dto(external.get("fisiologia"))

        deportes = external.get("deportes", [])
        return PerfilDemograficoDTO(
            tipo_identificacion=external.get("tipo_identificacion"),
            identificacion=external.get("identificacion"),
            reportes_sanguineo=[],
            demografia=demografia,
            fisiologia=fisiologia,
            deportes=deportes,
        )

    def dto_to_external(self, dto: PerfilDemograficoDTO) -> any:
        return asdict(dto)


class PerfilDemograficoDTODictMapper(ApplicationMapper):

    def _external_to_clasificacion_dto(self, external: dict) -> ClasificacionRiesgoDTO:
        imc: IndiceMasaCorporalDTO = IndiceMasaCorporalDTO(
            external.get("imc", {}).get("valor", 0.0),
            external.get("imc", {}).get("categoria", ""),
        )
        vo_max: VolumenMaximoOxigenoDTO = VolumenMaximoOxigenoDTO(
            external.get("vo_max", {}).get("valor", 0.0),
            external.get("vo_max", {}).get("categoria", ""),
        )
        return ClasificacionRiesgoDTO(
            imc=imc, vo_max=vo_max, riesgo=external.get("riesgo", "")
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

    def _external_to_demografia_dto(self, external: dict) -> InformacionDemograficaDTO:
        return InformacionDemograficaDTO(
            external.get("pais"),
            external.get("ciudad"),
        )

    def _external_to_fisiolofia_dto(self, external: dict) -> InformacionFisiologicaDTO:
        return InformacionFisiologicaDTO(
            external.get("genero"),
            int(external.get("edad")),
            float(external.get("altura")),
            float(external.get("peso")),
        )

    def external_to_dto(self, external: dict) -> PerfilDemograficoDTO:
        clasificacion_riesgo = self._external_to_clasificacion_dto(
            external.get("clasificacion_riesgo")
        )
        reportes_sanguineo = self._external_to_reportes_sanguineo_dto(
            external.get("reportes_sanguineo")
        )
        demografia = self._external_to_demografia_dto(external.get("demografia"))
        fisiologia = self._external_to_fisiolofia_dto(external.get("fisiologia"))
        return PerfilDemograficoDTO(
            tipo_identificacion=external.get("tipo_identificacion", ""),
            identificacion=external.get("identificacion", ""),
            clasificacion_riesgo=clasificacion_riesgo,
            reportes_sanguineo=reportes_sanguineo,
            demografia=demografia,
            fisiologia=fisiologia,
            deportes=external.get("deportes", []),
        )

    def dto_to_external(self, dto: PerfilDemograficoDTO) -> any:
        return asdict(dto)


class HabitoDTODictMapper(ApplicationMapper):
    def external_to_dto(self, external: dict) -> HabitoDeportivoDTO:

        return HabitoDeportivoDTO(
            tipo_identificacion=external.get("tipo_identificacion", ""),
            identificacion=external.get("identificacion", ""),
            titulo=external.get("titulo", ""),
            frecuencia=external.get("frecuencia", ""),
            descripcion=external.get("descripcion"),
        )

    def dto_to_external(self, dto: HabitoDeportivoDTO) -> dict:
        return asdict(dto)


class MolestiaDTODictMapper(ApplicationMapper):
    def external_to_dto(self, external: dict) -> MolestiaDTO:

        return MolestiaDTO(
            tipo_identificacion=external.get("tipo_identificacion", ""),
            identificacion=external.get("identificacion", ""),
            titulo=external.get("titulo", ""),
            fecha=external.get("fecha", ""),
            descripcion=external.get("descripcion"),
            tipo=external.get("tipo"),
        )

    def dto_to_external(self, dto: MolestiaDTO) -> dict:
        return asdict(dto)


class PerfilDeportivoDTODictMapper(ApplicationMapper):
    def external_to_habitos_dto(self, external: list[dict]) -> HabitoDeportivoDTO:
        habitos = list[HabitoDeportivoDTO] = []
        for habito in external:
            habitos.append(
                HabitoDeportivoDTO(
                    titulo=habito.get("titulo"),
                    frecuencia=habito.get("frecuencia"),
                    descripcion=habito.get("descripcion"),
                    tipo_identificacion=habito.get("tipo_identificacion"),
                    identificacion=habito.get("identificacion"),
                )
            )

        return habitos

    def external_to_molestias_dto(self, external: list[dict]) -> MolestiaDTO:
        molestias = list[MolestiaDTO] = []
        for molestia in external:
            molestias.append(
                MolestiaDTO(
                    titulo=molestia.get("titulo"),
                    tipo=molestia.get("tipo"),
                    descripcion=molestia.get("descripcion"),
                    fecha=molestia.get("fecha"),
                    tipo_identificacion=molestia.get("tipo_identificacion"),
                    identificacion=molestia.get("identificacion"),
                )
            )

        return molestias

    def external_to_dto(self, external: dict) -> PerfilDeportivoDTO:

        return PerfilDeportivoDTO(
            tipo_identificacion=external.get("tipo_identificacion", ""),
            identificacion=external.get("identificacion", ""),
            habitos=self.external_to_habitos_dto(
                external.get("habitos_deportivos", [])
            ),
            molestias=self.external_to_molestias_dto(external.get("molestias", [])),
        )

    def dto_to_external(self, dto: PerfilDeportivoDTO) -> dict:
        return asdict(dto)


class AlimentoDTODictMapper(ApplicationMapper):
    def external_to_dto(self, external: dict) -> AlimentoDTO:
        return AlimentoDTO(
            external.get("id", ""),
            external.get("nombre", ""),
            external.get("categoria", ""),
            external.get("tipo", ""),
        )

    def dto_to_external(self, dto: AlimentoDTO) -> dict:
        return asdict(dto)


class PerfilAlimenticioDTODictMapper(ApplicationMapper):
    def external_to_dto(self, external: dict) -> PerfilAlimenticioDTO:
        mapper = AlimentoDTODictMapper()
        alimentos = [mapper.external_to_dto(a) for a in external.get("alimentos", [])]
        return PerfilAlimenticioDTO(
            tipo_identificacion=external.get("tipo_identificacion", ""),
            identificacion=external.get("identificacion", ""),
            tipo_alimentacion=external.get("tipo_alimentacion", None),
            alimentos=alimentos,
        )

    def dto_to_external(self, dto: PerfilAlimenticioDTO) -> dict:
        return asdict(dto)


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
        vo_max = VolumenMaximoOxigeno(
            dto.clasificacion_riesgo.vo_max.valor,
            CategoriaVOM.get(
                dto.clasificacion_riesgo.vo_max.valor,
                dto.fisiologia.genero,
                dto.fisiologia.edad,
            ),
        )
        clasificacion = ClasificacionRiesgo(fisiologia.calculate_imc(), vo_max)
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
            VolumenMaximoOxigenoDTO(
                entity.clasificacion_riesgo.vo_max.valor,
                entity.clasificacion_riesgo.vo_max.categoria,
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


class HabitoDTOEntityMapper(DomainMapper):
    def type(self) -> type:
        return HabitoDeportivo

    def dto_to_entity(self, dto: HabitoDeportivoDTO) -> HabitoDeportivo:

        return HabitoDeportivo(
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
            titulo=dto.titulo,
            descripcion=dto.descripcion,
            frecuencia=dto.frecuencia,
        )

    def entity_to_dto(self, entity: HabitoDeportivo) -> HabitoDeportivoDTO:
        return HabitoDeportivoDTO(
            entity.titulo,
            entity.frecuencia,
            entity.descripcion,
            entity.tipo_identificacion,
            entity.identificacion,
        )


class MolestiaDTOEntityMapper(DomainMapper):
    def type(self) -> type:
        return Molestia

    def dto_to_entity(self, dto: MolestiaDTO) -> Molestia:

        return Molestia(
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
            titulo=dto.titulo,
            descripcion=dto.descripcion,
            tipo=dto.tipo,
            fecha=dto.fecha,
        )

    def entity_to_dto(self, entity: Molestia) -> MolestiaDTO:
        return MolestiaDTO(
            entity.titulo,
            entity.tipo,
            entity.fecha,
            entity.descripcion,
            entity.tipo_identificacion,
            entity.identificacion,
        )


class PerfilDeportivoDTOEntityMapper(DomainMapper):
    def type(self) -> type:
        return PerfilDeportivo

    def dto_to_entity(self, dto: PerfilDeportivoDTO) -> PerfilDeportivo:

        return PerfilDeportivo(
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
            habitos_deportivos=dto.habitos,
            molestias=dto.molestias,
        )

    def entity_to_dto(self, entity: PerfilDeportivo) -> PerfilDeportivoDTO:
        habitos = [
            HabitoDTOEntityMapper().entity_to_dto(h) for h in entity.habitos_deportivos
        ]
        molestias = [
            MolestiaDTOEntityMapper().entity_to_dto(h) for h in entity.molestias
        ]
        return PerfilDeportivoDTO(
            tipo_identificacion=entity.tipo_identificacion,
            identificacion=entity.identificacion,
            habitos=habitos,
            molestias=molestias,
        )


class AlimentoDTOEntityMapper(DomainMapper):
    def type(self) -> type:
        return Alimento

    def dto_to_entity(self, dto: AlimentoDTO) -> Alimento:
        args = [UUID(dto.id)] if dto.id else []
        return Alimento(
            *args, nombre=dto.nombre, categoria=dto.categoria, tipo=dto.tipo
        )

    def entity_to_dto(self, entity: Alimento) -> AlimentoDTO:
        return AlimentoDTO(
            id=entity.id,
            nombre=entity.nombre,
            categoria=entity.categoria,
            tipo=entity.tipo,
        )


class AlimentoAsociadoDTOEntityMapper(UnidirectionalDomainMapper):
    def type(self) -> type:
        return AlimentoAsociado

    def map(
        self,
        dto: AlimentoDTO,
        tipo_identificacion: str = None,
        identificacion: str = None,
    ) -> AlimentoAsociado:
        return AlimentoAsociado(
            id_alimento=dto.id,
            tipo_identificacion=tipo_identificacion,
            identificacion=identificacion,
            tipo=dto.tipo,
        )


class PerfilAlimenticioDTOEntityMapper(DomainMapper):
    def type(self) -> type:
        return PerfilAlimenticio

    def dto_to_entity(self, dto: PerfilAlimenticioDTO) -> PerfilAlimenticio:
        return PerfilAlimenticio(
            tipo_identificacion=dto.tipo_identificacion,
            identificacion=dto.identificacion,
            tipo_alimentacion=dto.tipo_alimentacion,
            alimentos=dto.alimentos,
        )

    def entity_to_dto(self, entity: PerfilAlimenticio) -> PerfilAlimenticioDTO:
        mapper = AlimentoDTOEntityMapper()
        alimentos = [mapper.entity_to_dto(h) for h in entity.alimentos]
        return PerfilAlimenticioDTO(
            tipo_identificacion=entity.tipo_identificacion,
            identificacion=entity.identificacion,
            tipo_alimentacion=entity.tipo_alimentacion,
            alimentos=alimentos,
        )
