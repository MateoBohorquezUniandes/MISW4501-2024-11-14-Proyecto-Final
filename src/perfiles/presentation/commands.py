from uuid import UUID

from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from perfiles.application.commands.associate_alimento import AssociateAlimento
from perfiles.application.commands.create_alimento import CreateAlimento
from perfiles.application.commands.update_clasificacion_riesgo import (
    ActualizarClasificacionRiesgo,
)
import seedwork.presentation.api as api
from perfiles.application.commands.crear_habito_deportivo import CrearHabitoDeportivo
from perfiles.application.commands.crear_molestia import CrearMolestia
from perfiles.application.commands.create_perfil_inicial import PerfilamientoInicial
from perfiles.application.mappers import (
    AlimentoDTODictMapper,
    HabitoDTODictMapper,
    MolestiaDTODictMapper,
    PerfilDemograficoDTODictMapper,
    PerfilamientoInicialDTODictMapper,
)
from perfiles.application.queries.get_perfil_demografico import ObtenerPerfilDemografico
from seedwork.application.commands import execute_command
from seedwork.application.queries import execute_query

bp_prefix: str = "/perfiles/commands"
bp: Blueprint = api.create_blueprint("commands", bp_prefix)


@bp.route("/demografico/init", methods=("POST",))
def create():
    mapper = PerfilamientoInicialDTODictMapper()
    data = request.json
    pefil_demografico_dto = mapper.external_to_dto(data.get("payload"))

    command = PerfilamientoInicial(
        correlation_id=UUID(data.get("correlation_id")),
        perfil_dto=pefil_demografico_dto,
    )
    execute_command(command)
    return {}, 202


@bp.route("/demografico/riesgo", methods=("PATCH",))
def actualizar_riesgo_perfil():
    mapper = PerfilDemograficoDTODictMapper()

    payload = request.json
    correlation_id = (
        UUID(payload["correlation_id"]) if "correlation_id" in payload else None
    )

    query_result = execute_query(
        ObtenerPerfilDemografico(
            tipo_identificacion=payload["payload"].get("tipo_identificacion"),
            identificacion=payload["payload"].get("identificacion"),
        )
    )
    vo_max_perfil = query_result.result.clasificacion_riesgo.vo_max.valor
    perfil_dict = mapper.dto_to_external(query_result.result)

    vo_max = payload.get("payload", {}).get("vo_max", vo_max_perfil)
    perfil_dict["clasificacion_riesgo"]["vo_max"]["valor"] = vo_max
    perfil_dto = mapper.external_to_dto(perfil_dict)

    command = ActualizarClasificacionRiesgo(
        correlation_id=correlation_id,
        perfil_dto=perfil_dto,
    )
    execute_command(command)
    return {}, 202


@bp.route("/deportivo/habitos", methods=("POST",))
@jwt_required()
def crear_habito_deportivo():
    mapper = HabitoDTODictMapper()
    data = request.json
    identificacion: dict = get_jwt_identity()
    payload = data.get("payload")
    payload["identificacion"] = identificacion.get("valor")
    payload["tipo_identificacion"] = identificacion.get("tipo")
    habito_dto = mapper.external_to_dto(payload)

    command = CrearHabitoDeportivo(habito_dto=habito_dto)

    execute_command(command)
    return {}, 202


@bp.route("/deportivo/molestias", methods=("POST",))
@jwt_required()
def crear_molestias():
    mapper = MolestiaDTODictMapper()
    data = request.json
    identificacion: dict = get_jwt_identity()
    payload = data.get("payload")
    payload["identificacion"] = identificacion.get("valor")
    payload["tipo_identificacion"] = identificacion.get("tipo")
    molestia_dto = mapper.external_to_dto(payload)

    command = CrearMolestia(molestia_dto=molestia_dto)

    execute_command(command)
    return {}, 202


@bp.route("/alimentos", methods=("POST",))
def crear_alimento():
    alimento_dto = AlimentoDTODictMapper().external_to_dto(request.json)
    command = CreateAlimento(alimento_dto=alimento_dto)

    execute_command(command)
    return {}, 202


@bp.route("/alimenticio/alimentos", methods=("POST",))
@jwt_required()
def asociar_alimento():
    identificacion: dict = get_jwt_identity()
    alimento_dto = AlimentoDTODictMapper().external_to_dto(request.json)

    command = AssociateAlimento(
        alimento_dto=alimento_dto,
        tipo_identificacion=identificacion.get("tipo"),
        identificacion=identificacion.get("valor"),
    )

    execute_command(command)
    return {}, 202
