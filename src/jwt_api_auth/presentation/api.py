from flask import (Blueprint, Response, redirect, render_template, request, session, url_for)
import seedwork.presentation.api as api
from seedwork.application.commands import execute_command
from seedwork.application.queries import execute_query as query
from jwt_api_auth.application.mappers import CreateTokenJsonMapper
from jwt_api_auth.application.commands.create_token import CreateToken

bp: Blueprint = api.create_blueprint("token", "/jwt")

@bp.route("create", methods=("POST",))
def create_token():
    request_create = request.json
    if(request.user and request.password):
        mapper = CreateTokenJsonMapper()
        token_dto = mapper.external_to_dto(request_create)
        comando = CreateToken(token_dto)
        token = execute_command(comando)
        return Response(token, status=200, mimetype="application/json")
    return Response({}, status=400)

@bp.route("validate", methods=("GET",))
def validate_token():
    #response = 
    return Response("{}", status=200, mimetype="application/json")