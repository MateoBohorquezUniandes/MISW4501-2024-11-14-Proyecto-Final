from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

import seedwork.presentation.api as api
from seedwork.application.queries import execute_query
from indicadores.application.mappers import FormulaDTODictMapper, IndicadoresDTODictMapper
from indicadores.application.queries.get_form_user import GetFormulas
from indicadores.application.queries.get_indicador_sesion import GetIndicadorSesion
#from sesiones.application.commands.create_sesion import CreateSesionDeportiva
#from sesiones.application.commands.end_sesion import EndSesionDeportiva

TIPO_GLOBAL = "global"
IDENTIFICACION_GLOBAL = "global"

bp_prefix: str = "/indices/queries"
bp: Blueprint = api.create_blueprint("queries", bp_prefix)
@bp.route("/", methods=("GET",))
def get_indicador_by_session():
    idSesion = request.args.get("idSesion", None)
    mapper = IndicadoresDTODictMapper()
    query_result = execute_query(GetIndicadorSesion(session_id=idSesion))  
    return jsonify([mapper.dto_to_external(e) for e in query_result.result])

@bp.route("/formula", methods=("GET",))
@jwt_required()
def get_formula_user():
    global_forms = request.args.get("global", None)
    if(global_forms != None and global_forms == "True"):
        tipo_identificacion = TIPO_GLOBAL
        identificacion = IDENTIFICACION_GLOBAL
    else:
        identidad: dict = get_jwt_identity()
        tipo_identificacion = identidad.get("tipo")
        identificacion = identidad.get("valor")

    mapper = FormulaDTODictMapper()
    query_result = execute_query(GetFormulas(tipo_identificacion=tipo_identificacion, identificacion=identificacion))  
    return jsonify([mapper.dto_to_external(e) for e in query_result.result])