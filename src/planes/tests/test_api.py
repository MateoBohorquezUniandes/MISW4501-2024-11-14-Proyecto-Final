import json
from http import HTTPStatus

import pytest

from planes.app import create_app
from planes.infrastructure.db import db
from planes.infrastructure.dtos import Entrenamiento, PlanEntrenamiento, UsuarioPlan


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

    @pytest.fixture(scope="function", autouse=True)
    def clear_tables(self):
        """
        Function fixture for cleaning the database tables
        before each test case
        """
        db.session.query(Entrenamiento).delete()
        db.session.query(PlanEntrenamiento).delete()
        db.session.query(UsuarioPlan).delete()
        db.session.commit()

    def test_create_plan_success(self, test_client):
        """Creacion exitosa de un usuario deportista"""
        payload = {
            "nombre": "Fortalecimiento Espalda",
            "categoria": "Fortalecimiento",
            "descripcion": "Fortalece los musculos de tu espalda con este plan de entrenamiento",
            "objetivo": {"exigencia": "Principiante", "deporte": "Ciclismo"},
        }

        response = test_client.post("/planes/", json=payload)
        assert response.status_code == HTTPStatus.ACCEPTED.value

    def test_create_entrenamiento_success(self, test_client):
        """Creacion exitosa de un usuario deportista"""
        payload = {
            "correlation_id": "dfebc03f-c6be-48b2-bb5f-4e49bddec908",
            "nombre": "Leg Press",
            "descripcion": "Entrenamiento de gluteos con maquina",
            "grupo_muscular": "gluteos",
            "imagen": "https://imagenes.com/gluteos.png",
            "duracion": {"valor": 10, "unidad": "reps", "series": 4},
        }

        response = test_client.post("/planes/entrenamientos", json=payload)
        assert response.status_code == HTTPStatus.ACCEPTED.value

    def test_create_usuario_success(self, test_client):
        """Creacion exitosa de un usuario deportista"""
        payload = {
            "correlation_id": "dfebc03f-c6be-48b2-bb5f-4e49bddec908",
            "specversion": "v1",
            "type": "event",
            "datacontenttype": "application/json",
            "payload": {
                "created_at": "2024-04-10T02:02:01Z",
                "tipo_identificacion": "CC",
                "identificacion": "23456789",
                "clasificacion_riesgo": {
                    "imc": {"valor": 21.76, "categoria": "Peso Normal"},
                    "riesgo": "Bajo",
                },
                "demografia": {"pais": "Colombia", "ciudad": "Bogota"},
                "fisiologia": {"genero": "M", "edad": 30, "altura": 7.8, "peso": 70.5},
                "deportes": ["Ciclismo"],
            },
        }

        response = test_client.post("/planes/entrenamientos", json=payload)
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
