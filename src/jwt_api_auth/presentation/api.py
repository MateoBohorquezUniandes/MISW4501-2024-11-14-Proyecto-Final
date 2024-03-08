from flask import (Blueprint, Response, redirect, render_template, request, session, url_for)
import seedwork.presentation.api as api
from seedwork.application.commands import execute_command
from seedwork.application.queries import execute_query as query
from jwt_api_auth.application.mappers import CreateTokenJsonMapper
from jwt_api_auth.application.commands.create_token_alt import  CreateTokenHandler
from jwt_api_auth.application.queries.validate_token import  ValidateTokenHandler

bp: Blueprint = api.create_blueprint("token", "/jwt")

@bp.route("create", methods=("POST",))
def create_token():
    request_create = request.json
    if(request_create.get("user") and request_create.get("password")):
        #mapper = CreateTokenJsonMapper()
        #token_dto = mapper.external_to_dto(request_create)
        token = CreateTokenHandler().create(request_create.get("user"), request_create.get("password"))
        return token, 200
    return Response({}, status=400)


@bp.route("validate", methods=("GET",))
def validate_token():
    authorization = request.headers.get('Authorization')
    if (authorization):
        token = authorization.split(' ')[-1]  
        validation = ValidateTokenHandler().create(token)
        return validation, 200
    return Response({}, status=400)

# Consumo Create Token
"""
import requests

url = 'https://jsonplaceholder.typicode.com/users'
#url = os.environ.get("JWT_URL")

data = {'user': "Mateo", 'password': 'mateo'}

response = requests.post(
    url,
    data=data,
    timeout=30
)

json_data = response.json()

token = json_data.get("accessToken")
"""

# Consumo Validate Token
"""
import requests

url = 'https://jsonplaceholder.typicode.com/users'
#url = os.environ.get("JWT_URL")

authorization = request.headers.get('Authorization')
token = authorization.split(' ')[-1]

headers = {
    "Authorization": "Bearer " + str(token),
}

response = requests.get(
    url,
    headers=headers,
    timeout=30
)

json_data = response.json()

isValidToken = json_data.get("isValid")
"""