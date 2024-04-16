from flask import Blueprint, Response, jsonify, request

import seedwork.presentation.api as api
from seedwork.application.commands import CommandResult, execute_command
from usuarios.application.commands.create_usuario import CreateUsuario
from usuarios.application.commands.login_usuario import LoginUsuario
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
