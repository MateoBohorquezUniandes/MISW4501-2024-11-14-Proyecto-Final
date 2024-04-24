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
    query_result = execute_query(GetEventos())
    return jsonify([mapper.dto_to_external(e) for e in query_result.result])
