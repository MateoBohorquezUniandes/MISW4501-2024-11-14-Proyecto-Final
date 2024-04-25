import json
import pytest

from http import HTTPStatus
from flask_jwt_extended import create_access_token

from productos.app import create_app
from productos.infrastructure.db import db


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
            db.create_all()
            yield testing_client
            db.session.close()

    def test_add_evento_suecess(self, test_client):
        test_user = {
            "tipo": "CC",
            "valor": "111111111",
        }
        payload = {
            "tipo": "Alimentacion",
            "nombre": "super bicicleta",
            "descripcion": "el mejor producto para tu bicicleta",
            "imagen": "https://www.wikihow.com",
            "precio": 2500000,
            "deporte": "Ciclismo",
        }
        test_token = create_access_token(identity=test_user)
        response = test_client.post(
            "/productos/commands/",
            headers={"Authorization": f"Bearer {test_token}"},
            json={"payload": payload},
        )
        assert response.status_code == HTTPStatus.ACCEPTED.value

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
