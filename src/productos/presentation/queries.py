import seedwork.presentation.api as api
from seedwork.application.queries import execute_query

from flask import Blueprint, Response, jsonify, request
from productos.application.mappers import ProductoDTODictMapper
from productos.application.queries.get_productos import GetProductos

bp_prefix: str = "/productos/queries"
bp: Blueprint = api.create_blueprint("queries", bp_prefix)


@bp.route("/", methods=("GET",))
def get_productos():
    mapper = ProductoDTODictMapper()
    args = request.args
    deporte = args.get("deporte")
    tipo = args.get("tipo")

    query_result = execute_query(GetProductos(deporte=deporte, tipo=tipo))
    return jsonify([mapper.dto_to_external(e) for e in query_result.result])
