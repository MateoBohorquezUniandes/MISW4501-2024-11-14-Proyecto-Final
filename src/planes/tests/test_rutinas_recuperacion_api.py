from http import HTTPStatus

from planes.domain.value_objects import DEPORTE, DURACION_UNIDAD
import pytest
from flask_jwt_extended import create_access_token

from planes.app import create_app
from planes.infrastructure.db import db
from planes.infrastructure.dtos import RutinaRecuperacion


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
        db.session.query(RutinaRecuperacion).delete()
        db.session.commit()

    def test_create_rutina_recuperacion_success(self, test_client):
        """Creacion exitosa de un usuario deportista"""
        payload = {
            "nombre": "Recuperacion Espalda",
            "descripcion": "Recuperate despues de un ejercicio",
            "imagen": "https://imagen.fake.com",
            "deporte": DEPORTE.CILICMO.value,
            "frecuencia": {
                "valor": 10.0,
                "unidad": DURACION_UNIDAD.MINUTOS.value,
            },
        }

        response = test_client.post(
            "/planes/commands/rutinas/recuperacion", json=payload
        )
        assert response.status_code == HTTPStatus.ACCEPTED.value
