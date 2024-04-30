from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from perfiles.application.queries.get_perfil_alimenticio import ObtenerPerfilAlimenticio
from perfiles.application.queries.get_perfil_deportivo import ObtenerPerfilDeportivo
import seedwork.presentation.api as api
from perfiles.application.mappers import (
    PerfilAlimenticioDTODictMapper,
    PerfilDemograficoDTODictMapper,
    PerfilDeportivoDTODictMapper,
)
from perfiles.application.queries.get_perfil_demografico import ObtenerPerfilDemografico
from perfiles.application.queries.get_perfiles import GetPerfilesDeportivos
from seedwork.application.queries import execute_query

bp_prefix: str = "/perfiles/queries"
bp: Blueprint = api.create_blueprint("queries", bp_prefix)


@bp.route("/demografico", methods=("GET",))
@jwt_required()
def get_perfil_demografico(id=None):
    identificacion: dict = get_jwt_identity()
    query_result = execute_query(
        ObtenerPerfilDemografico(
            tipo_identificacion=identificacion.get("tipo"),
            identificacion=identificacion.get("valor"),
        )
    )
    mapper = PerfilDemograficoDTODictMapper()
    return jsonify(mapper.dto_to_external(query_result.result))


@bp.route("/deportivos", methods=("GET",))
def get_perfiles_deportivos():

    mapper = PerfilDeportivoDTODictMapper()
    query_result = execute_query(GetPerfilesDeportivos())
    return jsonify([mapper.dto_to_external(e) for e in query_result.result])


@bp.route("/deportivo", methods=("GET",))
@jwt_required()
def get_perfil_alimenticio():
    identificacion: dict = get_jwt_identity()
    query_result = execute_query(
        ObtenerPerfilDeportivo(
            tipo_identificacion=identificacion.get("tipo"),
            identificacion=identificacion.get("valor"),
        )
    )
    mapper = PerfilDeportivoDTODictMapper()

    return jsonify(mapper.dto_to_external(query_result.result))


@bp.route("/alimenticio", methods=("GET",))
@jwt_required()
def get_perfil_deportivo():
    identificacion: dict = get_jwt_identity()
    query_result = execute_query(
        ObtenerPerfilAlimenticio(
            tipo_identificacion=identificacion.get("tipo"),
            identificacion=identificacion.get("valor"),
        )
    )
    mapper = PerfilAlimenticioDTODictMapper()

    return jsonify(mapper.dto_to_external(query_result.result))
