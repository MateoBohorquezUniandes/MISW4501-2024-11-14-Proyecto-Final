import json
from http import HTTPStatus

import pytest

from autenticador.app import create_app


class TestOperations:
    @pytest.fixture(scope="session")
    def test_client(self):
        """
        Session fixtue for handling the lifecycle of the databse
        used for testing
        """
        app = create_app()
        testing_client = app.test_client()

        with app.app_context():
            yield testing_client

    def test_auth_success(self, test_client):
        """Creacion exitosa de un usuario deportista"""
        payload = {"tipo": "CC", "valor": "123456789"}

        response = test_client.post("/auth/", json=payload)
        assert response.status_code == HTTPStatus.OK.value

    def test_health(self, test_client):
        """Tests health check endpoint"""
        response = test_client.get("/health")
        assert response.status_code == HTTPStatus.OK.value

    def test_spec(self, test_client):
        """Tests health check endpoint"""
        response = test_client.get("/spec")
        assert response.status_code == HTTPStatus.OK.value

        data = json.loads(response.data)
        assert "info" in data
