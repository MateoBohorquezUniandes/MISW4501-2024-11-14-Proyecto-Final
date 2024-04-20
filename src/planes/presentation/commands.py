from uuid import UUID

from flask import Blueprint, Response, jsonify, request

import seedwork.presentation.api as api
from planes.application.commands.asociar_entrenamiento import AsociarEntrenamientos
from planes.application.commands.asociar_plan_entrenamiento import (
    CreateRecomendacionPlan,
)
from planes.application.commands.create_entrenamiento import CreateEntrenamiento
from planes.application.commands.create_plan_entrenamiento import (
    CreatePlanEntrenamiento,
)
from planes.application.mappers import (
    EntrenamientoDTODictMapper,
    PlanEntrenamientoDTODictMapper,
    UsuarioPlanDTODictMapper,
)
from seedwork.application.commands import execute_command

bp_prefix: str = "/planes/commands"
bp: Blueprint = api.create_blueprint("commands", bp_prefix)


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
