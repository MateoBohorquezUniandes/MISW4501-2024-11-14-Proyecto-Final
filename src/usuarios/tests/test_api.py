import json
from http import HTTPStatus

import pytest

from usuarios.app import create_app
from usuarios.infrastructure.db import db
from usuarios.infrastructure.dtos import Usuario


class TestOperations:
    USER_PASSWORD = "password"

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

    @pytest.fixture(scope="function", autouse=True)
    def clear_user_table(self):
        """
        Function fixture for cleaning the database tables
        before each test case
        """
        db.session.query(Usuario).delete()
        db.session.commit()

    def test_create_success(self, test_client):
        """Creacion exitosa de un usuario deportista"""
        payload = {
            "nombre": "Pepito",
            "apellido": "Perez",
            "rol": "DEPORTISTA",
            "planAfiliacion":"GRATUITO",
            "contrasena": "contrasena123456",
            "identificacion": {"tipo": "DNI", "valor": "12345678901"},
            "demografia": {
                "pais_nacimiento": "Colombia",
                "ciudad_nacimiento": "Bogota",
                "pais_residencia": "Colombia",
                "ciudad_residencia": "Bogota",
                "tiempo_residencia": 30,
                "genero": "M",
                "edad": 30,
                "peso": 50.0,
                "altura": 1.60,
            },
            "deportes": ["ciclismo"],
        }

        response = test_client.post("/usuarios/", json=payload)
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
