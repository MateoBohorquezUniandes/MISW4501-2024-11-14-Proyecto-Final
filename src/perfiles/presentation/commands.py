from uuid import UUID

from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

import seedwork.presentation.api as api
from perfiles.application.commands.crear_habito_deportivo import CrearHabitoDeportivo
from perfiles.application.commands.create_perfil_inicial import PerfilamientoInicial
from perfiles.application.commands.crear_molestia import CrearMolestia
from perfiles.application.mappers import (
    HabitoDTODictMapper,
    PerfilDemograficoJsonDtoMapper,
    MolestiaDTODictMapper,
)
from seedwork.application.commands import execute_command

bp_prefix: str = "/perfiles/commands"
bp: Blueprint = api.create_blueprint("commands", bp_prefix)


@bp.route("/demografico/init", methods=("POST",))
def create():
    mapper = PerfilDemograficoJsonDtoMapper()
    data = request.json
    pefil_demografico_dto = mapper.external_to_dto(data.get("payload"))

    command = PerfilamientoInicial(
        correlation_id=UUID(data.get("correlation_id")),
        perfil_dto=pefil_demografico_dto,
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

    print(molestia_dto)
    command = CrearMolestia(molestia_dto=molestia_dto)

    execute_command(command)
    return {}, 202
