import json
from os import environ

import requests
from google.cloud import tasks_v2

from seedwork.infrastructure.dispatchers import Dispatcher
from seedwork.infrastructure.schema.v1.messages import IntegrationMessage
from usuarios.infrastructure.factories import IntegrationMessageFactory


class UsuarioIntegrationEventDispatcher(Dispatcher):
    def __init__(self, event):
        self._integration_factory = IntegrationMessageFactory()
        self._message: IntegrationMessage = self._integration_factory.create(event)

    def publish(self, url):
        client = tasks_v2.CloudTasksClient()

        task = tasks_v2.Task(
            http_request=tasks_v2.HttpRequest(
                http_method=tasks_v2.HttpMethod.POST,
                url=url,
                headers={"Content-type": self._message.datacontenttype},
                body=json.dumps(self._message).encode(),
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
