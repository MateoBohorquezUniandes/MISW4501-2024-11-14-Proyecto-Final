from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

import seedwork.presentation.api as api
from seedwork.application.commands import CommandResult, execute_command
from usuarios.application.commands.create_usuario import CreateUsuario
from usuarios.application.commands.login_usuario import LoginUsuario
from usuarios.application.commands.patch_afiliacion import ActualizarAfiliacion
from usuarios.application.mappers import (
    AuthResponseDTODictMapper,
    LoginDTODictMapper,
    UsuarioDTODictMapper,
)

bp_prefix: str = "/usuarios/commands"
bp: Blueprint = api.create_blueprint("commands", bp_prefix)


@bp.route("/", methods=("POST",))
def create():
    data = request.json
    mapper = UsuarioDTODictMapper()
    usuario_dto = mapper.external_to_dto(data)

    command = CreateUsuario(usuario_dto=usuario_dto)
    execute_command(command)

    return {}, 202


@bp.route("/login", methods=("POST",))
def login():
    data = request.json
    login_mapper = LoginDTODictMapper()
    login_dto = login_mapper.external_to_dto(data)

    command = LoginUsuario(login_request=login_dto)
    command_response: CommandResult = execute_command(command)

    auth_mapper = AuthResponseDTODictMapper()
    result = auth_mapper.dto_to_external(command_response.result)

    return jsonify(result)


@bp.route("/afiliacion", methods=("PATCH",))
@jwt_required()
def actualizar_afiliacion():
    identificacion: dict = get_jwt_identity()
    command = ActualizarAfiliacion(
        tipo_identificacion=identificacion.get("tipo"),
        identificacion=identificacion.get("valor"),
        plan_afiliacion=request.json.get("plan_afiliacion", ""),
    )
    execute_command(command)

    return {}, 202
