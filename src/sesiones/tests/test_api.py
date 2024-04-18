import json
from http import HTTPStatus
import uuid

import pytest

from sesiones.app import create_app
from sesiones.infrastructure.db import db
from sesiones.infrastructure.dtos import SesionDeportiva
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
    def test_sesion_dto(self):
        """
        Function fixture for creating an initial user
        as a precondition for some test cases
        """
        sesion = SesionDeportiva(
            id=uuid.uuid4(),
            tipo_identificacion=self.identificacion["tipo"],
            identificacion=self.identificacion["valor"],
            exigencia="Intermedio",
            deporte="Ciclismo",
        )
        db.session.add(sesion)
        db.session.commit()

        return sesion

    @pytest.fixture(scope="function", autouse=True)
    def clear_tables(self):
        """
        Function fixture for cleaning the database tables
        before each test case
        """
        yield
        db.session.query(SesionDeportiva).delete()
        db.session.commit()

    @pytest.fixture(scope="function")
    def session_token(self):
        """
        Function fixture for creating a session token
        """
        token = create_access_token(identity=self.identificacion)
        return token

    def test_create_sesion_success(self, test_client, session_token):
        """Creacion exitosa de un usuario deportista"""
        response = test_client.post(
            "/sesiones/commands/",
            headers={"Authorization": f"Bearer {session_token}"},
            json={
                "objetivo": {"exigencia": "Principiante", "deporte": "Ciclismo"},
            },
        )
        assert response.status_code == HTTPStatus.OK.value

    def test_end_sesion_success(self, test_client, session_token, test_sesion_dto):
        """Creacion exitosa de un usuario deportista"""
        response = test_client.put(
            "/sesiones/commands/",
            headers={"Authorization": f"Bearer {session_token}"},
            json={
                "id": test_sesion_dto.id,
                "parametros": {
                    "postencia": [100, 100, 200, 300],
                    "ritmo_cardiaco": [100, 100, 200, 300],
                },
            },
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
