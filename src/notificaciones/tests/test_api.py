import json
from notificaciones.infrastructure.firebase_messaging import MessageAdmin
import pytest

from http import HTTPStatus
from unittest.mock import patch

from notificaciones.app import create_app


class TestOperations:
    @pytest.fixture(scope="session")
    def test_client(self):
        """
        Session fixtue for handling the lifecycle of the databse
        used for testing
        """
        app = create_app()
        testing_client = app.test_client()

        yield testing_client

    def test_subscribe_to_topic_success(self, test_client):
        with patch.object(MessageAdmin, "subscribe_topic") as mock_method:
            mock_method.return_value = True

            payload = {
                "registration_tokens": ["1315665465464"],
                "topic": "test",
            }

            response = test_client.post(
                "/notificaciones/commands/suscribir",
                json=payload,
            )
            assert response.status_code == HTTPStatus.CREATED.value

    def test_send_to_topic_success(self, test_client):
        with patch.object(MessageAdmin, "send_topic_push") as mock_method:
            mock_method.return_value = True

            payload = {"titulo": "my test", "topic": "test", "body": "the best test"}
            response = test_client.post(
                "/notificaciones/commands/enviar-topico",
                json=payload,
            )
            assert response.status_code == HTTPStatus.CREATED.value

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
