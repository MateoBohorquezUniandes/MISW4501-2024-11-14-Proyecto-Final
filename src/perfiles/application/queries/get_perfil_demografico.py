from seedwork.application.queries import Query, QueryHandler, QueryResult
from seedwork.application.queries import execute_query
from dataclasses import dataclass, field
import perfiles.domain.value_objects as vo
import perfiles.domain.entities as ent


@dataclass(frozen=True)
class ObtenerPerfilDemografico(Query):
    id: str = field(default_factory=str)


class ObtenerPerfilDemograficoQueryHandler(QueryHandler):

    def handle(self, query: ObtenerPerfilDemografico) -> QueryResult:
        from uuid import uuid4

        id_usuario = uuid4()
        clasificacion_riesgo = vo.ClasificacionRiesgo(50.0, vo.CategoriaRiesgo.MODERADA)

        reporte_sanguineo = [
            ent.ReporteSanguineo(
                resultados=[
                    vo.ResultadoElementoSanguineo(
                        vo.ExamenSanguineo.GLUCOSA, 50.0, "ml/g"
                    )
                ]
            ),
            ent.ReporteSanguineo(
                resultados=[
                    vo.ResultadoElementoSanguineo(
                        vo.ExamenSanguineo.COLESTEROL, 60.0, "ml/g"
                    )
                ]
            ),
        ]
        reporte_demografico = vo.InformacionDemografica("Colombia")
        fisiologia = vo.InformacionFisiologica(25, 180.0, 70.3)

        return QueryResult(
            result=ent.PerfilDemografico(
                id_usuario=id_usuario,
                clasificacion_riesgo=clasificacion_riesgo,
                reporte_sanguineo=reporte_sanguineo,
                reporte_demografico=reporte_demografico,
                fisiologia=fisiologia
            )
        )


@execute_query.register(ObtenerPerfilDemografico)
def execute_query_perfil_demografico(query: ObtenerPerfilDemografico):
    return ObtenerPerfilDemograficoQueryHandler().handle(query)