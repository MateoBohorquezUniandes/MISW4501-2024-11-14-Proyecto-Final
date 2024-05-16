from http import HTTPStatus

import pytest
from flask_jwt_extended import create_access_token

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

    @pytest.fixture(scope="function")
    def test_db_perfil(self):
        """
        Function fixture for creating an initial perfil
        as a precondition for some test cases
        """
        perfil = PerfilDemografico()
        perfil.tipo_identificacion = "CC"
        perfil.identificacion = "111111111"
        perfil.clasificacion_riesgo = "Muy Bajo"
        perfil.vo_max_cateroria = "Excelente"
        perfil.vo_max_valor = 35.0
        perfil.imc_valor = 22.5
        perfil.imc_cateroria = "Peso Normal"
        perfil.genero = "F"
        perfil.edad = 28
        perfil.peso = 80.0
        perfil.altura = 1.79
        perfil.pais = "Colombia"
        perfil.ciudad = "wewew"
        db.session.add(perfil)
        db.session.commit()

        yield perfil

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

    def test_add_reporte_sanguineo_success(self, test_client, test_db_perfil):
        test_user = {
            "tipo": test_db_perfil.tipo_identificacion,
            "valor": test_db_perfil.identificacion,
        }
        payload = {"tipo_examen": "Creatinina", "valor": 2.5, "unidad": "mg/dL"}
        test_token = create_access_token(identity=test_user)
        response = test_client.post(
            "/perfiles/commands/demografico/reporte-sanguineo",
            headers={"Authorization": f"Bearer {test_token}"},
            json={"resultado": payload},
        )
        assert response.status_code == HTTPStatus.ACCEPTED.value

    def test_update_demografico_fisiologia_success(self, test_client, test_db_perfil):
        test_user = {
            "tipo": test_db_perfil.tipo_identificacion,
            "valor": test_db_perfil.identificacion,
        }
        payload = {"fisiologia": {"peso": 75.8, "altura": 1.79}}
        test_token = create_access_token(identity=test_user)
        response = test_client.patch(
            "/perfiles/commands/demografico/fisiologia",
            headers={"Authorization": f"Bearer {test_token}"},
            json={"payload": payload},
        )
        assert response.status_code == HTTPStatus.ACCEPTED.value
