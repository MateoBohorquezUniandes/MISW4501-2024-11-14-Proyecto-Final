from http import HTTPStatus

import pytest

from perfiles.app import create_app
from perfiles.infrastructure.db import db
from perfiles.infrastructure.dtos import PerfilDemografico, ReporteSanguineo


class TestPerfilDemograficoAPI:
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
        db.session.commit()

    def test_init_perfil_success(self, test_client):
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
                }
            },
        }

        response = test_client.post("/perfiles/commands/demografico/init", json=payload)
        assert response.status_code == HTTPStatus.ACCEPTED.value
