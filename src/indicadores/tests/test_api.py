import json
from http import HTTPStatus
import uuid

import pytest

from indicadores.app import create_app
from indicadores.infrastructure.db import db
from indicadores.infrastructure.dtos import Formula
from flask_jwt_extended import create_access_token


class TestOperations:

    identificacion = {"tipo": "CC", "valor": "123456789"}

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

    @pytest.fixture(scope="function")
    def session_token(self):
        """
        Function fixture for creating a session token
        """
        token = create_access_token(identity=self.identificacion)
        return token

    def test_create_formula_success(self, test_client, session_token):
        """Creacion de una formula"""
        response = test_client.post(
            "/indicadores/commands/formula",
            headers={"Authorization": f"Bearer {session_token}"},
            json={
                "nombre": "test",
                "descripcion": "test",
                "formula": "x + y**3",
                "parametros": {
                    "potencia": {"simbolo": "x", "funcion": "max"},
                    "ritmo_cardiaco": {"simbolo": "y", "funcion": "avg"},
                },
            },
        )
        assert response.status_code == HTTPStatus.CREATED.value

    def test_recalculate_success(self, test_client, session_token):
        """Creacion de indicador recalculando"""
        response = test_client.put(
            "/indicadores/commands/",
            headers={"Authorization": f"Bearer {session_token}"},
            json={
                "correlation_id": "d7f94c6a-3e39-4d13-a7ea-614e1b94c333",
                "specversion": "v1",
                "type": "event",
                "datacontenttype": "application/json",
                "payload": {
                    "id": "",
                    "tipo_identificacion": "CC",
                    "identificacion": "123456789",
                    "parametros": {
                        "potencia": [185, 192, 200, 202, 197, 175],
                        "ritmo_cardiaco": [132, 159, 165, 170, 173, 168],
                    },
                },
            },
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
