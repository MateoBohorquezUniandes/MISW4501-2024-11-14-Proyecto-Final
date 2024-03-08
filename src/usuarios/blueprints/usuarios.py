from flask import Blueprint, Flask, g, jsonify, request
from flask_jwt_extended import jwt_required

import seedwork.presentation.api as api
from usuarios.commands.crear_usuario import CrearUsuario
from usuarios.commands.db_restore import db_restore
from usuarios.commands.generar_token import create_token
from usuarios.errors.errors import InformacionIncompleta, InformacionIncompletaNoValida
from usuarios.models.model import Usuario, UsuarioSchema, db
from http import HTTPStatus

import requests
import os
import logging
import random

logging.basicConfig(format="%(message)s", level=logging.INFO)
log = logging.getLogger(__name__)

usuario_schema = UsuarioSchema()

bp_prefix: str = "/usuarios"
bp: Blueprint = api.create_blueprint("usuarios", bp_prefix)

bp = Blueprint("usuarios", __name__)
base_url = os.environ["JWt_BASE_URL"]
JWT_VALIDATE_URL = f"{base_url}/validate"


@bp.route("/", methods=["POST"])
def create_user():
    data = request.json
    if all(
        fields in data
        for fields in (
            "nombre_usuario",
            "apellido_usuario",
            "tipo_identificacion",
            "numero_identificacion",
            "genero",
            "edad",
            "peso",
            "altura",
            "pais_nacimiento",
            "ciudad_nacimiento",
            "pais_residencia",
            "ciudad_residencia",
            "antiguedad_residencia",
            "deportes_practicar",
            "role_usuario",
            "password",
        )
    ):
        command = CrearUsuario(
            nombre_usuario=data["nombre_usuario"],
            apellido_usuario=data["apellido_usuario"],
            tipo_identificacion=data["tipo_identificacion"],
            numero_identificacion=data["numero_identificacion"],
            genero=data["genero"],
            edad=data["edad"],
            peso=data["peso"],
            altura=data["altura"],
            pais_nacimiento=data["pais_nacimiento"],
            ciudad_nacimiento=data["ciudad_nacimiento"],
            pais_residencia=data["pais_residencia"],
            ciudad_residencia=data["ciudad_residencia"],
            antiguedad_residencia=data["antiguedad_residencia"],
            deportes_practicar=data["deportes_practicar"],
            role_usuario=data["role_usuario"],
            password=data["password"],
        )
        usuario = command.execute()
        # token_de_acceso = create_access_token(identity=usuario.id)

        return (
            jsonify(id=usuario.id, fechaCreacion=usuario.createdAt),
            201,
        )
    else:
        raise InformacionIncompletaNoValida


@bp.route("/autenticar", methods=["POST"])
def generate_token():
    data = request.json
    if all(fields in data for fields in ("nombre_usuario", "password")):

        usuario = Usuario.query.filter_by(nombre_usuario=data["nombre_usuario"]).first()

        command = create_token(
            nombre_usuario=data["nombre_usuario"], password=data["password"]
        )
        result, status_code = command.execute()
        return jsonify(result), status_code
    else:
        raise InformacionIncompleta


@bp.route("/", methods=["GET"])
@jwt_required()
def listar_usuarios():
    usuarios = Usuario.query.all()
    return [usuario_schema.dump(usuario) for usuario in usuarios]


@bp.route("/me/<nombre>", methods=["GET"])
@jwt_required()
def get_usuario(nombre: str):
    usuario = Usuario.query.filter_by(nombre_usuario=nombre).first()

    token = request.headers["Authorization"]
    header = {"Authorization": token}

    response = requests.get(JWT_VALIDATE_URL, headers=header)

    if response.status_code != 200:
        raise HTTPStatus.UNAUTHORIZED.value

    auth_data = response.json()
    is_valid_token = auth_data.get("isValid")
    if is_valid_token == False:
        raise HTTPStatus.UNAUTHORIZED.value
    log.info(f'{auth_data["message"]["user"]} and {usuario.nombre_usuario}')
    usuario_from_token = auth_data["message"]["user"]

    if usuario.nombre_usuario != usuario_from_token:
        raise HTTPStatus.UNAUTHORIZED.value
    return usuario_schema.dump(usuario)


@bp.route("/reset", methods=["DELETE"])
@jwt_required()
def clear_data():
    db_restore.execute()
    return jsonify({"msg": "OK"}, 200)


@bp.route("/healthexperimento", methods=["GET"])
def health_experimento():
    fail_rate = float(os.environ["FAIL_RATE"])
    r = random.random()
    if r > fail_rate:
        raise HTTPStatus.INTERNAL_SERVER_ERROR.value
    else:
        return jsonify({"msg": "OK"}, 200)
