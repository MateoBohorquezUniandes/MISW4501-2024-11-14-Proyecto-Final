from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

import seedwork.presentation.api as api
from seedwork.application.queries import execute_query
from usuarios.application.mappers import (AuthResponseDTODictMapper,
                                          LoginDTODictMapper,
                                          UsuarioDTODictMapper)
from usuarios.application.queries.get_usuario import ObtenerUsuario

bp_prefix: str = "/usuarios/queries"
bp: Blueprint = api.create_blueprint("queries", bp_prefix)


@bp.route("/", methods=("GET",))
@jwt_required()
def get_usuario():
    identificacion: dict = get_jwt_identity()
    query_result = execute_query(
        ObtenerUsuario(
            tipo_identificacion=identificacion.get("tipo", ""),
            identificacion=identificacion.get("valor", ""),
            rol=identificacion.get("rol", ""),
        )
    )

    mapper = UsuarioDTODictMapper()
    return jsonify(mapper.dto_to_external(query_result.result))
