from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required


from seedwork.application.commands import execute_command
import seedwork.presentation.api as api

from eventos.application.mappers import EventoDTODictMapper
from eventos.application.commands.create_evento import CreateEvento

bp_prefix: str = "/eventos/commands"
bp: Blueprint = api.create_blueprint("commands", bp_prefix)


@bp.route("/", methods=("POST",))
@jwt_required()
def crear_habito_deportivo():
    mapper = EventoDTODictMapper()
    data = request.json
    # identificacion: dict = get_jwt_identity()
    payload = data.get("payload")
    # payload["identificacion"] = identificacion.get("valor")
    # payload["tipo_identificacion"] = identificacion.get("tipo")
    evento_dto = mapper.external_to_dto(payload)

    command = CreateEvento(evento_dto=evento_dto)

    execute_command(command)
    return {}, 202
