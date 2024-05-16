from dataclasses import dataclass

from perfiles.domain.entities import (
    Alimento,
    HabitoDeportivo,
    PerfilAlimenticio,
    PerfilDemografico,
    PerfilDeportivo,
    Molestia,
    ReporteSanguineo,
)
from perfiles.domain.events import PerfilDemograficoModified
from perfiles.domain.value_objects import AlimentoAsociado
from perfiles.infrastructure.exceptions import InvalidRepositoryFactoryException
from perfiles.infrastructure.repositories import (
    AlimentoAsociadoRepositoryPostgreSQL,
    AlimentoRepositoryPostgreSQL,
    HabitoDeportivoRepositoryPostgreSQL,
    PerfilAlimenticioRepositoryPostgreSQL,
    PerfilDemograficoRepositoryPostgreSQL,
    PerfilDeportivoRepositoryPostgreSQL,
    MolestiaRepositoryPostgreSQL,
    ReporteSanguineoRepositoryPostgreSQL,
)
from perfiles.infrastructure.schema.v1.mappers import (
    DemograficoModifiedIntegrationEventMapper,
)
from seedwork.domain.factories import Factory


@dataclass
class RepositoryFactory(Factory):
    def create(self, obj):
        if isinstance(obj, PerfilDemografico) or obj == PerfilDemografico:
            return PerfilDemograficoRepositoryPostgreSQL()
        elif isinstance(obj, PerfilDeportivo) or obj == PerfilDeportivo:
            return PerfilDeportivoRepositoryPostgreSQL()
        elif isinstance(obj, PerfilAlimenticio) or obj == PerfilAlimenticio:
            return PerfilAlimenticioRepositoryPostgreSQL()
        elif isinstance(obj, HabitoDeportivo) or obj == HabitoDeportivo:
            return HabitoDeportivoRepositoryPostgreSQL()
        elif isinstance(obj, Molestia) or obj == Molestia:
            return MolestiaRepositoryPostgreSQL()
        elif isinstance(obj, Alimento) or obj == Alimento:
            return AlimentoRepositoryPostgreSQL()
        elif isinstance(obj, AlimentoAsociado) or obj == AlimentoAsociado:
            return AlimentoAsociadoRepositoryPostgreSQL()
        elif isinstance(obj, ReporteSanguineo) or obj == ReporteSanguineo:
            return ReporteSanguineoRepositoryPostgreSQL()
        else:
            raise InvalidRepositoryFactoryException()


class IntegrationMessageFactory(Factory):
    def create(self, event: any) -> any:
        if type(event) is PerfilDemograficoModified:
            mapper = DemograficoModifiedIntegrationEventMapper()
            return mapper.external_to_message(event)
        else:
            raise InvalidRepositoryFactoryException()
