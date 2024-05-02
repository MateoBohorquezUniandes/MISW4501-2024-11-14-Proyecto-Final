from uuid import UUID

from flask import Blueprint, Response, jsonify, request

from planes.application.commands.create_rutina_alimentacion import (
    CreateRutinaAlimentacion,
)
import seedwork.presentation.api as api
from planes.application.commands.asociar_plan_entrenamiento import (
    CreateRecomendacionPlan,
)
from planes.application.commands.create_plan_entrenamiento import (
    CreatePlanEntrenamiento,
)
from planes.application.mappers import (
    EntrenamientoDTODictMapper,
    ObjetivoEntrenamientoDTODictMapper,
    PlanEntrenamientoDTODictMapper,
    RutinaAlimentacionDTODictMapper,
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


@bp.route("/rutinas", methods=("POST",))
def create_rutina_alimentacion():
    data: dict = request.json
    correlation_id = data.pop("correlation_id", None)

    mapper = RutinaAlimentacionDTODictMapper()
    rutina_dto = mapper.external_to_dto(data)

    command = CreateRutinaAlimentacion(correlation_id, rutina_dto)
    execute_command(command)

    return {}, 202


@bp.route("/asociar", methods=("POST",))
def associate_plan_entrenamiento():
    data: dict = request.json
    correlation_id = None
    if "correlation_id" in data:
        correlation_id = UUID(data.get("correlation_id"))

    payload: dict = data.get("payload")
    usuario_dto = UsuarioPlanDTODictMapper().external_to_dto(payload)
    deportes = payload.get("deportes", [])

    objetivo_dict = dict(
        deporte=deportes[0] if len(deportes) else None,
        exigencia=payload.get("clasificacion_riesgo", {}).get("riesgo", None),
    )
    objetivo_dto = ObjetivoEntrenamientoDTODictMapper().external_to_dto(objetivo_dict)

    command = CreateRecomendacionPlan(correlation_id, usuario_dto, objetivo_dto)
    execute_command(command)
    return {}, 202
