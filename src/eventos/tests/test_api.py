import json
import pytest

from http import HTTPStatus
from flask_jwt_extended import create_access_token

from perfiles.infrastructure.dtos import PerfilDeportivo

from eventos.app import create_app
from eventos.infrastructure.db import db


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
            "tipo": "ciclismo",
            "fecha": "2024-10-05",
            "lugar": "Medellin",
            "distancia": 1.5,
            "nivel": "Principiante",
            "nombre": "gran carrera",
        }
        test_token = create_access_token(identity=test_user)
        response = test_client.post(
            "/eventos/commands/",
            headers={"Authorization": f"Bearer {test_token}"},
            json={"payload": payload},
        )
        assert response.status_code == HTTPStatus.ACCEPTED.value

    def test_get_eventos_suecess(self, test_client):
        test_user = {
            "tipo": "CC",
            "valor": "111111111",
        }

        test_token = create_access_token(identity=test_user)
        response = test_client.get(
            "/eventos/queries/", headers={"Authorization": f"Bearer {test_token}"}
        )
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
