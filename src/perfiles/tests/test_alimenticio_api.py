from http import HTTPStatus
from uuid import uuid4

import pytest
from flask_jwt_extended import create_access_token

from perfiles.app import create_app
from perfiles.domain.value_objects import CategoriaAlimento, CategoriaAsociacionAlimento
from perfiles.infrastructure.db import db
from perfiles.infrastructure.dtos import Alimento, AlimentoAsociado, PerfilAlimenticio


class TestPerfilDeportivoAPI:
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
        db.session.query(AlimentoAsociado).delete()
        db.session.query(Alimento).delete()
        db.session.query(PerfilAlimenticio).delete()
        db.session.commit()

    @pytest.fixture(scope="function")
    def test_db_perfil(self):
        """
        Function fixture for creating an initial perfil
        as a precondition for some test cases
        """
        perfil = PerfilAlimenticio()
        perfil.tipo_identificacion = "CC"
        perfil.identificacion = "222222222"
        db.session.add(perfil)
        db.session.commit()

        yield perfil

    @pytest.fixture(scope="function")
    def test_db_alimento(self):
        """
        Function fixture for creating an initial perfil
        as a precondition for some test cases
        """
        alimento = Alimento()
        alimento.id = str(uuid4())
        alimento.nombre = "Fresa"
        alimento.categoria = CategoriaAlimento.FRUTA.value
        db.session.add(alimento)
        db.session.commit()

        yield alimento

    @pytest.fixture(scope="function")
    def test_db_asociacion(self, test_db_perfil, test_db_alimento):
        """
        Function fixture for creating an initial perfil
        as a precondition for some test cases
        """
        asociacion = AlimentoAsociado()
        asociacion.id_alimento = test_db_alimento.id
        asociacion.tipo_identificacion = test_db_perfil.tipo_identificacion
        asociacion.identificacion = test_db_perfil.identificacion
        asociacion.tipo = CategoriaAsociacionAlimento.ALERGIA.value
        db.session.add(asociacion)
        db.session.commit()

        yield asociacion

    def test_create_alimento(self, test_client):
        payload = {
            "nombre": "Pollo",
            "categoria": CategoriaAlimento.PROTEINA.value,
        }

        response = test_client.post(
            "/perfiles/commands/alimentos",
            json=payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED.value

    def test_associate_alimento(self, test_client, test_db_perfil, test_db_alimento):
        payload = {
            "id": test_db_alimento.id,
            "nombre": test_db_alimento.nombre,
            "categoria": test_db_alimento.categoria,
            "tipo": CategoriaAsociacionAlimento.PREFERENCIA.value,
        }
        test_token = create_access_token(
            identity={
                "tipo": test_db_perfil.tipo_identificacion,
                "valor": test_db_perfil.identificacion,
            }
        )
        response = test_client.post(
            "/perfiles/commands/alimenticio/alimentos",
            headers={"Authorization": f"Bearer {test_token}"},
            json=payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED.value
        assert db.session.query(AlimentoAsociado).count() == 1

    def test_get_perfil_alimenticio(self, test_client, test_db_asociacion):
        test_token = create_access_token(
            identity={
                "tipo": test_db_asociacion.tipo_identificacion,
                "valor": test_db_asociacion.identificacion,
            }
        )
        response = test_client.get(
            "/perfiles/queries/alimenticio",
            headers={"Authorization": f"Bearer {test_token}"},
        )
        assert response.status_code == HTTPStatus.OK.value
        
        data = response.json["data"]
        assert "alimentos" in data
        
        alimentos = data["alimentos"]
        assert len(alimentos) > 0
        assert "tipo" in alimentos[0]
        assert alimentos[0]["tipo"] == test_db_asociacion.tipo
