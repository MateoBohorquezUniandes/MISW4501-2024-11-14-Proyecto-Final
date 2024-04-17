from uuid import UUID
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from perfiles.application.commands.create_perfil_inicial import PerfilamientoInicial
from perfiles.application.commands.crear_habito_deportivo import CrearHabitoDeportivo
import seedwork.presentation.api as api
from perfiles.application.mappers import PerfilDemograficoJsonDtoMapper, HabitoDTODictMapper,PerfilDeportivoDTODictMapper
from perfiles.application.queries.get_perfil_demografico import ObtenerPerfilDemografico
from perfiles.application.queries.get_perfiles import GetPerfilesDeportivos
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
        correlation_id=UUID(data.get("correlation_id")),
        perfiles_demografico_dto=pefil_demografico_dto,
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

@bp.route("/deportivo/habitos", methods=("POST",))
@jwt_required()
def crear_habito_deportivo():
    mapper = HabitoDTODictMapper()
    data = request.json
    identificacion: dict = get_jwt_identity()
    payload = data.get("payload")
    payload["identificacion"] = identificacion.get("valor")
    payload["tipo_identificacion"] = identificacion.get("tipo")
    habito_dto = mapper.external_to_dto(payload)

    command = CrearHabitoDeportivo(
        habito_dto=habito_dto
    )

    execute_command(command)
    return {}, 202

@bp.route("/deportivos", methods=("GET",))
def get_perfiles_deportivos():

    mapper = PerfilDeportivoDTODictMapper()
    query_result = execute_query(GetPerfilesDeportivos())
    return jsonify([mapper.dto_to_external(e) for e in query_result.result])
