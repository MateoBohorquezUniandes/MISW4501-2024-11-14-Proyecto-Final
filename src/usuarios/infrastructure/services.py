import os

import requests

from seedwork.infrastructure.services import HTTPService
from usuarios.domain.factories import UsuarioFactory


class UsuarioAuthorizationService(HTTPService):
    def __init__(self):
        self._usuario_factory: UsuarioFactory = UsuarioFactory()

    def request(self, data):
        url = os.environ.get("AUTH_BASE_URL")
        response = requests.post(url, json=data)
        return response.json()
