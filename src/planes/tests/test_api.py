import json
import uuid
from http import HTTPStatus

import pytest
from flask_jwt_extended import create_access_token

from planes.app import create_app
from planes.infrastructure.db import db
from planes.infrastructure.dtos import (
    Entrenamiento,
    PlanEntrenamiento,
    UsuarioPlan,
    recomendacion_table,
)


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
        db.session.query(recomendacion_table).delete()
        db.session.query(PlanEntrenamiento).delete()
        db.session.query(UsuarioPlan).delete()
        db.session.commit()

    @pytest.fixture(scope="function")
    def test_db_user(self):
        """
        Function fixture for creating an initial user
        as a precondition for some test cases
        """
        user = UsuarioPlan()
        user.id = str(uuid.uuid4())
        user.tipo_identificacion = "CC"
        user.identificacion = "111111111"
        db.session.add(user)
        db.session.commit()

        yield user

    @pytest.fixture(scope="function")
    def test_db_plan(self):
        """
        Function fixture for creating an initial plan
        as a precondition for some test cases
        """
        plan = PlanEntrenamiento()
        plan.id = str(uuid.uuid4())
        plan.nombre = "Plan Prueba"
        plan.descripcion = "descripcion de prueba"
        plan.categoria = "Resistencia"
        plan.nivel_exigencia = "Alta"
        plan.deporte_objetivo = "Ciclismo"

        db.session.add(plan)
        db.session.commit()

        yield plan

    def test_create_plan_success(self, test_client):
        """Creacion exitosa de un usuario deportista"""
        payload = {
            "nombre": "Fortalecimiento Espalda",
            "categoria": "Fortalecimiento",
            "descripcion": "Fortalece los musculos de tu espalda con este plan de entrenamiento",
            "objetivo": {"exigencia": "Principiante", "deporte": "Ciclismo"},
        }

        response = test_client.post("/planes/commands/", json=payload)
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

        response = test_client.post("/planes/commands/entrenamientos", json=payload)
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
                    "vo_max": {"valor": 0.0, "categoria": "Muy Pobre"},
                },
                "demografia": {"pais": "Colombia", "ciudad": "Bogota"},
                "fisiologia": {"genero": "M", "edad": 30, "altura": 7.8, "peso": 70.5},
                "deportes": ["Ciclismo"],
            },
        }

        response = test_client.post("/planes/commands/asociar", json=payload)
        assert response.status_code == HTTPStatus.ACCEPTED.value

    def test_create_usuario_existente_success(
        self, test_client, test_db_user, test_db_plan
    ):
        """Creacion exitosa de un usuario deportista"""
        payload = {
            "correlation_id": "dfebc03f-c6be-48b2-bb5f-4e49bddec908",
            "specversion": "v1",
            "type": "event",
            "datacontenttype": "application/json",
            "payload": {
                "created_at": "2024-04-10T02:02:01Z",
                "tipo_identificacion": test_db_user.tipo_identificacion,
                "identificacion": test_db_user.identificacion,
                "clasificacion_riesgo": {
                    "imc": {"valor": 21.76, "categoria": "Peso Normal"},
                    "riesgo": "Bajo",
                    "vo_max": {"valor": 0.0, "categoria": "Muy Pobre"},
                },
                "demografia": {"pais": "Colombia", "ciudad": "Bogota"},
                "fisiologia": {"genero": "M", "edad": 30, "altura": 7.8, "peso": 70.5},
                "deportes": [test_db_plan.deporte_objetivo],
            },
        }

        response = test_client.post("/planes/commands/asociar", json=payload)
        assert response.status_code == HTTPStatus.ACCEPTED.value

    def test_get_usuario_plan(self, test_client, test_db_user):
        test_user = {
            "tipo": test_db_user.tipo_identificacion,
            "valor": test_db_user.identificacion,
        }
        test_token = create_access_token(identity=test_user)
        response = test_client.get(
            "/planes/queries/usuarios",
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
