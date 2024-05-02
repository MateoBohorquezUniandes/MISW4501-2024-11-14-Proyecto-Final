from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from planes.application.queries.get_rutinas_alimentacion import GetRutinasAlimentacion
import seedwork.presentation.api as api
from planes.application.mappers import (
    EntrenamientoDTODictMapper,
    PlanEntrenamientoDTODictMapper,
    RutinaAlimentacionDTODictMapper,
    UsuarioPlanDTODictMapper,
)
from planes.application.queries.get_entrenamientos import GetEnternamientos
from planes.application.queries.get_planes_asociados_usuario import (
    GetPlanesAsociadosUsuario,
)
from planes.application.queries.get_planes_entrenamiento import GetPlanesEnternamiento
from planes.application.queries.get_usuarios import GetUsuarioPlanes
from seedwork.application.queries import execute_query

bp_prefix: str = "/planes/queries"
bp: Blueprint = api.create_blueprint("queries", bp_prefix)


@bp.route("/", methods=("GET",))
def get_planes_entrenamiento():
    mapper = PlanEntrenamientoDTODictMapper()
    query_result = execute_query(GetPlanesEnternamiento())
    return jsonify([mapper.dto_to_external(e) for e in query_result.result])


@bp.route("/entrenamientos", methods=("GET",))
def get_entrenamientos():
    mapper = EntrenamientoDTODictMapper()
    query_result = execute_query(GetEnternamientos())
    return jsonify([mapper.dto_to_external(e) for e in query_result.result])


@bp.route("/rutinas", methods=("GET",))
def get_rutinas_alimentacion():
    args = request.args
    deporte = args.get("deporte", None)
    tipo = args.get("tipo", None)
    mapper = RutinaAlimentacionDTODictMapper()
    query_result = execute_query(
        GetRutinasAlimentacion(deporte=deporte, tipo_alimentacion=tipo)
    )
    return jsonify([mapper.dto_to_external(e) for e in query_result.result])


@bp.route("/usuarios", methods=("GET",))
@jwt_required()
def get_usuario_plan():
    identificacion: dict = get_jwt_identity()
    mapper = UsuarioPlanDTODictMapper()
    result = None
    if identificacion:
        query_result = execute_query(
            GetPlanesAsociadosUsuario(
                tipo_identificacion=identificacion.get("tipo"),
                identificacion=identificacion.get("valor"),
            )
        )
        result = mapper.dto_to_external(query_result.result)
    else:
        query_result = execute_query(GetUsuarioPlanes())
        result = [mapper.dto_to_external(e) for e in query_result.result]
    return jsonify(result)
