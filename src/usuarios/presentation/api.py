from uuid import UUID
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from seedwork.application.commands import CommandResult, execute_command

import seedwork.presentation.api as api

from seedwork.application.queries import execute_query
from usuarios.application.commands.create_usuario import CreateUsuario
from usuarios.application.commands.login_usuario import LoginUsuario
from usuarios.application.mappers import (
    AuthResponseDTODictMapper,
    LoginDTODictMapper,
    UsuarioDTODictMapper,
)

bp_prefix: str = "/usuarios"
bp: Blueprint = api.create_blueprint("usuarios", bp_prefix)


@bp.route("/", methods=("POST",))
def create():
    data = request.json
    mapper = UsuarioDTODictMapper()
    usuario_dto = mapper.external_to_dto(data)
    correlation_id = (
        UUID(data.get("correlation_id", )) if "correlation_id" in data else None
    )

    command = CreateUsuario(usuario_dto=usuario_dto)
    execute_command(command)

    return {}, 202


@bp.route("/login", methods=("POST",))
def login():
    data = request.json
    login_mapper = LoginDTODictMapper()
    login_dto = login_mapper.external_to_dto(data)
    correlation_id = (
        UUID(data.get("correlation_id", )) if "correlation_id" in data else None
    )

    command = LoginUsuario(login_request=login_dto)
    command_response: CommandResult = execute_command(command)

    auth_mapper = AuthResponseDTODictMapper()
    result = auth_mapper.dto_to_external(command_response.result)

    return jsonify(result)
