from flask_jwt_extended import get_jwt_identity, jwt_required
from eventos.application.queries.get_eventos_asociados import ObtenerEventosAsociados
import seedwork.presentation.api as api
from seedwork.application.queries import execute_query

from flask import Blueprint, Response, jsonify, request
from eventos.application.mappers import EventoDTODictMapper
from eventos.application.queries.get_eventos import GetEventos

bp_prefix: str = "/eventos/queries"
bp: Blueprint = api.create_blueprint("queries", bp_prefix)


@bp.route("/", methods=("GET",))
def get_eventos():
    mapper = EventoDTODictMapper()
    args = request.args
    lugar = args.get("lugar")
    fecha = args.get("fecha")
    nivel = args.get("nivel")
    query_result = execute_query(GetEventos(lugar=lugar, fecha=fecha, nivel=nivel))
    return jsonify([mapper.dto_to_external(e) for e in query_result.result])


@bp.route("/asociados", methods=("GET",))
@jwt_required()
def get_perfil_alimenticio():
    identificacion: dict = get_jwt_identity()
    programado = bool(request.args.get("programado", 1, int))
    query_result = execute_query(
        ObtenerEventosAsociados(
            tipo_identificacion=identificacion.get("tipo"),
            identificacion=identificacion.get("valor"),
            programado=programado,
        )
    )
    mapper = EventoDTODictMapper()
    return jsonify([mapper.dto_to_external(e) for e in query_result.result])
