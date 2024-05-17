import json
from http import HTTPStatus
from uuid import uuid4

import pytest
from flask_jwt_extended import create_access_token

from seedwork.domain.value_objects import GENERO
from usuarios.app import create_app
from usuarios.domain.value_objects import PLAN_AFILIACION, ROL
from usuarios.infrastructure.db import db
from usuarios.infrastructure.dtos import Deportista, Usuario


class TestUserAPI:
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
        db.session.query(Deportista).delete()
        db.session.query(Usuario).delete()
        db.session.commit()

    @pytest.fixture(scope="function")
    def test_user_db(self):
        deportista_dto = Deportista()
        deportista_dto.tipo_identificacion = "CC"
        deportista_dto.identificacion = "123456789"
        deportista_dto.rol = ROL.DEPORTISTA.value
        deportista_dto.contrasena = self.USER_PASSWORD
        deportista_dto.salt = uuid4()

        deportista_dto.nombre = "John"
        deportista_dto.apellido = "Doe"
        deportista_dto.plan_afiliacion = PLAN_AFILIACION.GRATUITO.value
        deportista_dto.genero = GENERO
        deportista_dto.edad = 18
        deportista_dto.peso = 70.0
        deportista_dto.altura = 1.70
        deportista_dto.pais_nacimiento = "Colombia"
        deportista_dto.ciudad_nacimiento = "Bogota"
        deportista_dto.pais_residencia = "Colombia"
        deportista_dto.ciudad_residencia = "Bogota"
        deportista_dto.tiempo_residencia = 10
        deportista_dto.deportes = "Ciclismo"

        yield deportista_dto

    def test_create_success(self, test_client):
        """Creacion exitosa de un usuario deportista"""
        payload = {
            "nombre": "Pepito",
            "apellido": "Perez",
            "rol": "DEPORTISTA",
            "plan_afiliacion": PLAN_AFILIACION.GRATUITO.value,
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
            "deportes": ["Ciclismo"],
        }

        response = test_client.post("/usuarios/commands/", json=payload)
        assert response.status_code == HTTPStatus.ACCEPTED.value

    def path_user_afiliacion_success(self, test_client, test_user_db: Deportista):
        test_token = create_access_token(
            identity={
                "tipo": test_user_db.tipo_identificacion,
                "valor": test_user_db.identificacion,
                "rol": test_user_db.rol,
            }
        )
        payload = {"plan_afiliacion": PLAN_AFILIACION.INTERMEDIO.value}
        response = test_client.patch(
            "/usuarios/commands/afiliacion",
            headers={"Authorization": f"Bearer {test_token}"},
            json=payload,
        )
        assert response.status_code == HTTPStatus.OK.value

    def get_user_success(self, test_client, test_user_db: Deportista):
        test_token = create_access_token(
            identity={
                "tipo": test_user_db.tipo_identificacion,
                "valor": test_user_db.identificacion,
                "rol": test_user_db.rol,
            }
        )
        response = test_client.get(
            "/usuarios/queries/",
            headers={"Authorization": f"Bearer {test_token}"},
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
