from uuid import UUID
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from perfiles.application.commands.create_perfil_inicial import PerfilamientoInicial
import seedwork.presentation.api as api
from perfiles.application.mappers import PerfilDemograficoJsonDtoMapper
from perfiles.application.queries.get_perfil_demografico import ObtenerPerfilDemografico
from seedwork.application.queries import execute_query
from seedwork.application.commands import execute_command

bp_prefix: str = "/perfiles"
bp: Blueprint = api.create_blueprint("perfiles", bp_prefix)


@bp.route("/demografico/init", methods=("POST",))
def create():
    mapper = PerfilDemograficoJsonDtoMapper()
    data = request.json
    pefil_demografico_dto = mapper.external_to_dto(data.get("payload"))

    command = PerfilamientoInicial(
        perfiles_demografico_dto=pefil_demografico_dto,
        correlation_id=UUID(data.get("correlation_id")),
    )
    execute_command(command)

    return {}, 202


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
    mapper = PerfilDemograficoJsonDtoMapper()

    return jsonify(mapper.dto_to_external(query_result.result))
