import os

from seedwork.infrastructure.exceptions import MissingJWTSecrets

__author__ = "Santiago Cortés Fernández"
__email__ = "s.cortes@uniandes.edu.co"


def retrieve_secret_key() -> str:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

    if not JWT_SECRET_KEY:
        raise MissingJWTSecrets()

    return JWT_SECRET_KEY
