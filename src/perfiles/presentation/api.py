from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

import seedwork.presentation.api as api
from perfiles.application.mappers import PerfilDemograficoJsonDtoMapper
from perfiles.application.queries.get_perfil_demografico import ObtenerPerfilDemografico
from seedwork.application.queries import execute_query

bp_prefix: str = "/perfiles"
bp: Blueprint = api.create_blueprint("perfiles", bp_prefix)


@bp.route("/demograficos", methods=("GET",))
@bp.route("/demograficos/<id>", methods=("GET",))
@jwt_required()
def get_perfil_demografico(id=None):

    current_user = get_jwt_identity()
    query_result = execute_query(ObtenerPerfilDemografico(id))
    mapper = PerfilDemograficoJsonDtoMapper()

    return mapper.dto_to_external(query_result.result)
