from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required


from eventos.application.commands.asociar_evento import AssociateEvento
from seedwork.application.commands import execute_command
import seedwork.presentation.api as api

from eventos.application.mappers import EventoDTODictMapper
from eventos.application.commands.create_evento import CreateEvento

bp_prefix: str = "/eventos/commands"
bp: Blueprint = api.create_blueprint("commands", bp_prefix)


@bp.route("/", methods=("POST",))
@jwt_required()
def crear_evento():
    mapper = EventoDTODictMapper()
    data = request.json

    payload = data.get("payload")
    evento_dto = mapper.external_to_dto(payload)

    command = CreateEvento(evento_dto=evento_dto)

    execute_command(command)
    return {}, 202


@bp.route("/asociar", methods=("POST",))
@jwt_required()
def asociar_evento():
    identificacion: dict = get_jwt_identity()
    evento_dto = EventoDTODictMapper().external_to_dto(request.json)

    command = AssociateEvento(
        evento_dto=evento_dto,
        tipo_identificacion=identificacion.get("tipo"),
        identificacion=identificacion.get("valor"),
    )

    execute_command(command)
    return {}, 202
