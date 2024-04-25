import json
from dataclasses import asdict
from os import environ

from google.cloud import tasks_v2
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

    def publish(self, url):
        if self.__bypass:
            return
        
        client = IndicadoresAPIService()
        response: Response = client.request(
            "PUT", "indicadores/commands", asdict(self._message)
        )
        response.raise_for_status()


        # TODO agregar valor de vo2 max
        self._message.payload.vo_max = response.json().get("vo_max", 0.0)
        client = tasks_v2.CloudTasksClient()

        task = tasks_v2.Task(
            http_request=tasks_v2.HttpRequest(
                http_method=tasks_v2.HttpMethod.PATCH,
                url=url,
                headers={"Content-type": self._message.datacontenttype},
                body=json.dumps(asdict(self._message)).encode(),
            )
        )

        LOCATION_ID = environ.get("LOCATION_ID", "")
        PROJECT_ID = environ.get("PROJECT_ID", "")
        QUEUE_ID = environ.get("QUEUE_ID", "")

        parent = client.queue_path(PROJECT_ID, LOCATION_ID, QUEUE_ID)
        response = client.create_task(
            tasks_v2.CreateTaskRequest(
                parent=parent,
                task=task,
            )
        )

        return {
            "name": response.name,
            "http_request": {
                "url": response.http_request.url,
                "http_method": str(response.http_request.http_method),
            },
        }
