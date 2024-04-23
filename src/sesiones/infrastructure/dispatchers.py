from dataclasses import asdict
from os import environ

from requests import Response

from seedwork.infrastructure.dispatchers import Dispatcher
from seedwork.infrastructure.schema.v1.messages import IntegrationMessage
from seedwork.presentation.exceptions import APIError
from sesiones.infrastructure.factories import IntegrationMessageFactory
from sesiones.infrastructure.services import IndicadoresAPIService


class SesionIntegrationCommandDispatcher(Dispatcher):
    def __init__(self, event):
        self._integration_factory = IntegrationMessageFactory()
        self._message: IntegrationMessage = self._integration_factory.create(event)
        self.__bypass = environ.get("TESTING", "") == "True"

    def publish(self, path):
        if self.__bypass:
            return

        client = IndicadoresAPIService()
        response: Response = client.request("PUT", path, asdict(self._message))
        response.raise_for_status()

        return {
            "name": "IndicadoresAPIService",
            "http_request": {
                "url": response.request.url,
                "http_method": str(response.request.method),
            },
        }
