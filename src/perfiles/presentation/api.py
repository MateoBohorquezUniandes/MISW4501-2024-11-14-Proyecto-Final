from perfiles.application.mappers import PerfilDemograficoJsonDtoMapper
import seedwork.presentation.api as api
from flask import Blueprint, Response, jsonify, request

from perfiles.application.queries.get_perfil_demografico import \
    ObtenerPerfilDemografico
from seedwork.application.queries import execute_query

bp_prefix: str = "/perfiles"
bp: Blueprint = api.create_blueprint("perfiles", bp_prefix)


@bp.route("/demograficos", methods=("GET",))
@bp.route("/demograficos/<id>", methods=("GET",))
def get_perfil_demografico(id=None):
    query_result = execute_query(ObtenerPerfilDemografico(id))
    mapper = PerfilDemograficoJsonDtoMapper()
    
    return mapper.dto_to_external(query_result.result)
