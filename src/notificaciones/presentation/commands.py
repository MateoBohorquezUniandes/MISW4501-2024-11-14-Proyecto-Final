from firebase_admin import credentials, messaging
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

import seedwork.presentation.api as api


bp_prefix: str = "/notificaciones/commands"
bp: Blueprint = api.create_blueprint("commands", bp_prefix)


def subscribe_topic(tokens, topic):  # tokens is a list of registration tokens
    #   tokens = [
    #     'YOUR_REGISTRATION_TOKEN_1',
    #     # ...
    #     'YOUR_REGISTRATION_TOKEN_n',
    # ]
    response = messaging.subscribe_to_topic(tokens, topic)
    if response.failure_count > 0:
        print(
            f"Failed to subscribe to topic {topic} due to {list(map(lambda e: e.reason,response.errors))}"
        )
    print(response.success_count, "tokens were subscribed successfully")


def send_topic_push(title, body, topic):
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body), topic=topic
    )
    # message = messaging.Message(
    #     data={
    #         'score': '850',
    #         'time': '2:45',
    #     },
    #     topic=topic,
    # )
    # Send a message to the devices subscribed to the provided topic.
    response = messaging.send(message)
    # Response is a message ID string.
    print("Successfully sent message:", response)


@bp.route("/enviar-topico", methods=("POST",))
def send_notification():
    data = request.json
    topic = data.get("topic")
    titulo = data.get("titulo")
    body = data.get("body")
    send_topic_push(titulo, body, topic)
    return {}, 201


@bp.route("/suscribir", methods=("POST",))
def subscribe():
    data = request.json
    tokens = data.get("registration_tokens")
    topic = data.get("topic")
    subscribe_topic(tokens, topic)
    return {}, 201


@bp.route("/desuscribir", methods=("POST",))
def unsubscribe():
    data = request.json
    tokens = data.get("registration_tokens")
    topic = data.get("topic")
    # Unubscribe the devices corresponding to the registration tokens from the
    # topic.
    response = messaging.unsubscribe_from_topic(tokens, topic)
    # See the TopicManagementResponse reference documentation
    # for the contents of response.
    print(response.success_count, "tokens were unsubscribed successfully")
