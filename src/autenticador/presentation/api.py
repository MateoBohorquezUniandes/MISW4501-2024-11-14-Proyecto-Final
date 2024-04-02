from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from seedwork.application.commands import execute_command

import seedwork.presentation.api as api

from autenticador.application.commands.create_token import CreateToken
from autenticador.application.mappers import AuthDTODictMapper

bp_prefix: str = "/auth"
bp: Blueprint = api.create_blueprint("auth", bp_prefix)


@bp.route("/", methods=("POST",))
def create():
    mapper = AuthDTODictMapper()
    dto = mapper.external_to_dto(request.json)
    correlation_id = request.headers.get('correlation_id', None)

    command = CreateToken(request=dto, correlation_id=correlation_id)
    response = execute_command(command)
    token_resp = mapper.dto_to_external(response.result)
    print(token_resp)
    
    return jsonify(token_resp)
