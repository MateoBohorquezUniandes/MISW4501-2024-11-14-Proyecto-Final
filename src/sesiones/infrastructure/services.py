from os import environ
from flask import Response
import requests

from seedwork.infrastructure.services import HTTPService


class SesionAuthorizationService(HTTPService):
    def request(self, identificacion):
        url = environ.get("AUTH_BASE_URL")
        response = requests.post(url, json=identificacion)
        return response.json()


class IndicadoresAPIService(HTTPService):

    def request(self, method, path, payload=None) -> requests.Response:
        url = f"{environ.get('INDICADORES_BASE_URL')}/{path}"
        response = None
        if not payload:
            response = requests.request(method, url)
        else:
            response = requests.request(method, url, json=payload)
        return response
