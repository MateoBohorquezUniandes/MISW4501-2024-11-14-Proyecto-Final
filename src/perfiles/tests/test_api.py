import json
from http import HTTPStatus

import pytest
from flask_jwt_extended import create_access_token

from perfiles.app import create_app
from perfiles.infrastructure.db import db
from perfiles.infrastructure.dtos import (
    HabitoDeportivo,
    PerfilAlimenticio,
    PerfilDemografico,
    PerfilDeportivo,
    ReporteSanguineo,
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
    def clear_user_table(self):
        """
        Function fixture for cleaning the database tables
        before each test case
        """
        db.session.query(ReporteSanguineo).delete()
        db.session.query(PerfilDemografico).delete()
        db.session.query(PerfilDeportivo).delete()
        db.session.query(PerfilAlimenticio).delete()
        db.session.commit()

    @pytest.fixture(scope="function")
    def test_db_perfil(self):
        """
        Function fixture for creating an initial perfil
        as a precondition for some test cases
        """
        perfil = PerfilDeportivo()
        perfil.tipo_identificacion = "CC"
        perfil.identificacion = "111111111"
        db.session.add(perfil)
        db.session.commit()

        yield perfil
        db.session.query(HabitoDeportivo).delete()
        db.session.query(PerfilDeportivo).delete()
        db.session.commit()

    def test_create_success(self, test_client):
        """Creacion exitosa de un usuario deportista"""
        payload = {
            "correlation_id": "70f9a8c4-190f-49a2-9256-e0d4a4d2ab2a",
            "type": "event",
            "specversion": "v1",
            "datacontenttype": "application/json",
            "payload": {
                "tipo_identificacion": "CC",
                "identificacion": "123456789",
                "rol": "DEPORTISTA",
                "demografia": {
                    "pais_residencia": "Colombia",
                    "ciudad_residencia": "Bogota",
                },
                "fisiologia": {
                    "genero": "M",
                    "edad": "30",
                    "peso": "70.5",
                    "altura": "1.80",
                },
            },
        }

        response = test_client.post("/perfiles/commands/demografico/init", json=payload)
        assert response.status_code == HTTPStatus.ACCEPTED.value

    def test_add_habito_deportivo_suecess(self, test_client, test_db_perfil):
        test_user = {
            "tipo": test_db_perfil.tipo_identificacion,
            "valor": test_db_perfil.identificacion,
        }
        payload = {
            "titulo": "habito test",
            "descripcion": "este es un habito de prueba",
            "frecuencia": "Mensual",
        }
        test_token = create_access_token(identity=test_user)
        response = test_client.post(
            "/perfiles/commands/deportivo/habitos",
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
        assert "info" in data.get("data", {})
