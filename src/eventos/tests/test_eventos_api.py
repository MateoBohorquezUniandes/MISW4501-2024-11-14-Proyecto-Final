from datetime import datetime, timedelta
from http import HTTPStatus
from uuid import uuid4

import pytest
from flask_jwt_extended import create_access_token

from eventos.app import create_app
from eventos.infrastructure.db import db
from eventos.infrastructure.dtos import Evento, EventoAsociado
from eventos.domain.value_objects import EXIGENCIA
from seedwork.domain.value_objects import DEPORTE


class TestEventosAPI:
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
        db.session.query(EventoAsociado).delete()
        db.session.query(Evento).delete()
        db.session.commit()

    @pytest.fixture(scope="function")
    def test_db_evento(self):
        """
        Function fixture for creating an initial perfil
        as a precondition for some test cases
        """
        evento = Evento()
        evento.id = str(uuid4())
        evento.tipo = DEPORTE.CILICMO.value
        evento.fecha = datetime.utcnow() + timedelta(days=1)
        evento.lugar = "Bogota"
        evento.distancia = 1.5
        evento.nivel = EXIGENCIA.PRINCIPIANTE.value
        evento.nombre = "Carrera Test"

        db.session.add(evento)
        db.session.commit()

        yield evento

    @pytest.fixture(scope="function")
    def test_db_evento_asociado(self, test_db_evento):
        """
        Function fixture for creating an initial perfil
        as a precondition for some test cases
        """
        evento = EventoAsociado()
        evento.id = test_db_evento.id
        evento.tipo_identificacion = "CC"
        evento.identificacion = "123456789"
        evento.fecha = datetime.utcnow() + timedelta(days=1)

        db.session.add(evento)
        db.session.commit()

        yield evento

    def test_add_evento_success(self, test_client):
        test_user = {
            "tipo": "CC",
            "valor": "111111111",
        }
        payload = {
            "tipo": DEPORTE.CILICMO.value,
            "fecha": "2024-10-05",
            "lugar": "Medellin",
            "distancia": 1.5,
            "nivel": EXIGENCIA.PRINCIPIANTE.value,
            "nombre": "gran carrera",
        }
        test_token = create_access_token(identity=test_user)
        response = test_client.post(
            "/eventos/commands/",
            headers={"Authorization": f"Bearer {test_token}"},
            json={"payload": payload},
        )
        assert response.status_code == HTTPStatus.ACCEPTED.value

    def test_asociar_evento_success(self, test_client, test_db_evento: Evento):
        payload = {
            "id": test_db_evento.id,
            "tipo": test_db_evento.tipo,
            "fecha": str(test_db_evento.fecha),
            "lugar": test_db_evento.lugar,
            "distancia": test_db_evento.distancia,
            "nivel": test_db_evento.nivel,
            "nombre": test_db_evento.nombre,
        }
        test_token = create_access_token(identity=dict(tipo="CC", valor="123456789"))
        response = test_client.post(
            "/eventos/commands/asociar",
            headers={"Authorization": f"Bearer {test_token}"},
            json=payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED.value

    def test_get_eventos_success(self, test_client, test_db_evento):
        test_user = {
            "tipo": "CC",
            "valor": "111111111",
        }

        test_token = create_access_token(identity=test_user)
        response = test_client.get(
            "/eventos/queries/", headers={"Authorization": f"Bearer {test_token}"}
        )
        assert response.status_code == HTTPStatus.OK.value

    def test_get_eventos_asociados_programados_success(
        self, test_client, test_db_evento_asociado: EventoAsociado
    ):
        test_token = create_access_token(
            identity=dict(
                tipo=test_db_evento_asociado.tipo_identificacion,
                valor=test_db_evento_asociado.identificacion,
            )
        )
        response = test_client.get(
            "/eventos/queries/asociados",
            headers={"Authorization": f"Bearer {test_token}"},
        )
        assert response.status_code == HTTPStatus.OK.value

    def test_get_eventos_asociados_realizados_success(
        self, test_client, test_db_evento_asociado: EventoAsociado
    ):
        test_token = create_access_token(
            identity=dict(
                tipo=test_db_evento_asociado.tipo_identificacion,
                valor=test_db_evento_asociado.identificacion,
            )
        )
        response = test_client.get(
            "/eventos/queries/asociados?programado=0",
            headers={"Authorization": f"Bearer {test_token}"},
        )
        assert response.status_code == HTTPStatus.OK.value
