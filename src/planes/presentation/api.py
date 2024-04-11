from uuid import UUID

from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from planes.application.commands.asociar_entrenamiento import AsociarEntrenamientos
from planes.application.queries.get_usuarios import GetUsuarioPlanes
from planes.application.queries.get_planes_asociados_usuario import GetPlanesAsociadosUsuario
import seedwork.presentation.api as api
from planes.application.commands.asociar_plan_entrenamiento import CreateRecomendacionPlan
from planes.application.commands.create_entrenamiento import CreateEntrenamiento
from planes.application.commands.create_plan_entrenamiento import (
    CreatePlanEntrenamiento,
)
from planes.application.mappers import (
    EntrenamientoDTODictMapper,
    PlanEntrenamientoDTODictMapper,
    UsuarioPlanDTODictMapper,
)
from planes.application.queries.get_entrenamientos import GetEnternamientos
from planes.application.queries.get_planes_entrenamiento import GetPlanesEnternamiento
from seedwork.application.commands import execute_command
from seedwork.application.queries import execute_query

bp_prefix: str = "/planes"
bp: Blueprint = api.create_blueprint("planes", bp_prefix)


@bp.route("/entrenamientos", methods=("POST",))
def create_entrenamiento():
    data: dict = request.json
    correlation_id = None
    if "correlation_id" in data:
        correlation_id = UUID(data.get("correlation_id"))

    mapper = EntrenamientoDTODictMapper()
    entrenamiento_dto = mapper.external_to_dto(data)

    command = CreateEntrenamiento(correlation_id, entrenamiento_dto)
    execute_command(command)

    return {}, 202


@bp.route("/entrenamientos", methods=("GET",))
def get_entrenamientos():
    mapper = EntrenamientoDTODictMapper()
    query_result = execute_query(GetEnternamientos())

    return jsonify([mapper.dto_to_external(e) for e in query_result.result])


@bp.route("/", methods=("POST",))
def create_plan_entrenamiento():
    data = request.json
    correlation_id = None
    if "correlation_id" in data:
        correlation_id = UUID(data.get("correlation_id"))

    mapper = PlanEntrenamientoDTODictMapper()
    plan_dto = mapper.external_to_dto(data)

    command = CreatePlanEntrenamiento(correlation_id, plan_dto)
    execute_command(command)

    return {}, 202


@bp.route("/", methods=("PATCH",))
def asociar_entrenamientos():
    data = request.json
    correlation_id = None
    if "correlation_id" in data:
        correlation_id = UUID(data.get("correlation_id"))

    mapper = PlanEntrenamientoDTODictMapper()
    plan_dto = mapper.external_to_dto(data)

    command = AsociarEntrenamientos(correlation_id, plan_dto)
    execute_command(command)

    return {}, 202


@bp.route("/", methods=("GET",))
def get_planes_entrenamiento():

    mapper = PlanEntrenamientoDTODictMapper()
    query_result = execute_query(GetPlanesEnternamiento())

    return jsonify([mapper.dto_to_external(e) for e in query_result.result])


@bp.route("/asociar", methods=("POST",))
def associate_plan_entrenamiento():
    data: dict = request.json
    correlation_id = None
    if "correlation_id" in data:
        correlation_id = UUID(data.get("correlation_id"))

    payload = data.get("payload")
    mapper = UsuarioPlanDTODictMapper()
    usuario_dto = mapper.external_to_dto(payload)

    command = CreateRecomendacionPlan(
        correlation_id, usuario_dto, payload.pop("deportes", [])
    )
    execute_command(command)

    return {}, 202


@bp.route("/usuarios", methods=("GET",))
def get_usuarios_plan():

    mapper = UsuarioPlanDTODictMapper()
    query_result = execute_query(GetUsuarioPlanes())

    return jsonify([mapper.dto_to_external(e) for e in query_result.result])


@bp.route("/usuario", methods=("GET",))
@jwt_required()
def get_usuario_plan():
    identificacion: dict = get_jwt_identity()
    mapper = UsuarioPlanDTODictMapper()
    query_result = execute_query(
         GetPlanesAsociadosUsuario(
             tipo_identificacion=identificacion.get("tipo"),
             identificacion=identificacion.get("valor"),
         )
     )
    
    return jsonify(mapper.dto_to_external(query_result.result))