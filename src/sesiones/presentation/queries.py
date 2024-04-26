from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

import seedwork.presentation.api as api
from seedwork.application.queries import execute_query
from sesiones.application.queries.get_sesion import ObtenerSesion
from sesiones.application.mappers import SesionDeportivaDTODictMapper
from sesiones.application.queries.get_sesiones import ObtenerSesiones

bp_prefix: str = "/sesiones/queries"
bp: Blueprint = api.create_blueprint("queries", bp_prefix)


@bp.route("/", methods=("GET",))
@jwt_required()
def get_sesion():
    identity: dict = get_jwt_identity()
    tipo_identificacion = identity.get("tipo")
    identificacion = identity.get("valor")

    mapper = SesionDeportivaDTODictMapper()
    id = request.args.get("id", "")
    print(f"ID {id}")
    result = dict()
    if id:
        query_result = execute_query(
            ObtenerSesion(tipo_identificacion, identificacion, id)
        )
        result = mapper.dto_to_external(query_result.result)
    else:
        query_result = execute_query(
            ObtenerSesiones(tipo_identificacion, identificacion)
        )
        result = [mapper.dto_to_external(r) for r in query_result.result]

    return jsonify(result)
