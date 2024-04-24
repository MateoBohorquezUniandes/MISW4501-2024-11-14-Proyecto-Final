from seedwork.application.handlers import Handler
from sesiones.infrastructure.dispatchers import SesionIntegrationCommandDispatcher


class SesionEndedIntegrationMessageHandler(Handler):

    @staticmethod
    def handle(event):
        dispatcher = SesionIntegrationCommandDispatcher(event)
        dispatcher.publish("commands/indicadores")
