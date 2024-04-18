from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

import seedwork.presentation.api as api
from seedwork.application.commands import execute_command
from sesiones.application.commands.create_sesion import CreateSesionDeportiva
from sesiones.application.commands.end_sesion import EndSesionDeportiva
from sesiones.application.mappers import SesionDeportivaDTODictMapper

bp_prefix: str = "/sesiones/commands"
bp: Blueprint = api.create_blueprint("commands", bp_prefix)


@bp.route("/", methods=("POST",))
@jwt_required()
def create_sesion():
    identificacion: dict = get_jwt_identity()
    data: dict = request.json
    data["tipo_identificacion"] = identificacion.get("tipo")
    data["identificacion"] = identificacion.get("valor")

    mapper = SesionDeportivaDTODictMapper()
    sesion_dto = mapper.external_to_dto(data)

    command = CreateSesionDeportiva(sesion_dto=sesion_dto)
    command_result = execute_command(command)

    return jsonify(mapper.dto_to_external(command_result))


@bp.route("/", methods=("PUT",))
@jwt_required()
def end_sesion():
    identificacion: dict = get_jwt_identity()
    data: dict = request.json
    data["tipo_identificacion"] = identificacion.get("tipo")
    data["identificacion"] = identificacion.get("valor")
    parameters = data.pop("parametros", {})

    mapper = SesionDeportivaDTODictMapper()
    sesion_dto = mapper.external_to_dto(data)

    command = EndSesionDeportiva(sesion_dto=sesion_dto, parameters=parameters)
    execute_command(command)

    return {}, 202
