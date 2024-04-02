from seedwork.application.handlers import Handler
from usuarios.infrastructure.dispatchers import UserIntegrationEventDispatcher


class UsuarioCreatedIntegrationMessageHandler(Handler):

    @staticmethod
    def handle(event):
        dispatcher = UserIntegrationEventDispatcher(event)
        # dispatcher.publish("usuarios-events")