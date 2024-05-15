from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from notificaciones.application.commands.send_to_topic import SendToTopic
from notificaciones.application.commands.subscribe_to_topic import SubscribeToTopic
from notificaciones.application.mappers import (
    SendToTopicDTODictMapper,
    SubscribeToTopicDTODictMapper,
)
from seedwork.application.commands import execute_command
import seedwork.presentation.api as api


bp_prefix: str = "/notificaciones/commands"
bp: Blueprint = api.create_blueprint("commands", bp_prefix)


@bp.route("/enviar-topico", methods=("POST",))
def send_notification():
    data = request.json

    mapper = SendToTopicDTODictMapper()
    message_dto = mapper.external_to_dto(data)

    command = SendToTopic(message_dto=message_dto)
    execute_command(command)
    return {}, 201


@bp.route("/suscribir", methods=("POST",))
def subscribe():
    data = request.json
    mapper = SubscribeToTopicDTODictMapper()
    message_dto = mapper.external_to_dto(data)

    command = SubscribeToTopic(message_dto=message_dto)
    execute_command(command)
    return {}, 201
