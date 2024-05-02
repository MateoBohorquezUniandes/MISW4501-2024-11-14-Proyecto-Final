import uuid
from http import HTTPStatus

from planes.domain.value_objects import DEPORTE, PORCION_UNIDAD
import pytest
from flask_jwt_extended import create_access_token

from planes.app import create_app
from planes.infrastructure.db import db
from planes.infrastructure.dtos import GrupoAlimenticio, RutinaAlimentacion
from seedwork.domain.value_objects import CATEGORIA_ALIMENTO, TIPO_ALIMENTACION


class TestRutinasAlimentacionAPI:

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
        db.session.query(GrupoAlimenticio).delete()
        db.session.query(RutinaAlimentacion).delete()
        db.session.commit()

    def test_create_plan_success(self, test_client):
        """Creacion exitosa de un usuario deportista"""
        payload = {
            "nombre": "Fortalecimiento Espalda",
            "descripcion": "Alimentate con los mejores alimentos",
            "imagen": "https://imagen.fake.com",
            "tipo_alimentacion": TIPO_ALIMENTACION.VEGETARIANO.value,
            "deporte": DEPORTE.CILICMO.value,
            "grupos_alimenticios": [
                {
                    "grupo": CATEGORIA_ALIMENTO.VERDURA.value,
                    "porcion": 1.5,
                    "unidad": PORCION_UNIDAD.TAZA.value,
                    "calorias": 500.0
                }
            ],
        }

        response = test_client.post("/planes/commands/rutinas", json=payload)
        assert response.status_code == HTTPStatus.ACCEPTED.value
