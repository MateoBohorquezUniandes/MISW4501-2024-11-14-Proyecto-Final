import os

from seedwork.infrastructure.exceptions import (
    MissingDatabaseConfiguration,
    MissingDatabaseCredentials,
)

__author__ = "Santiago Cortés Fernández"
__email__ = "s.cortes@uniandes.edu.co"


def generate_database_uri(provider: str) -> str:
    """
    Generates the Database URI using the envrionment
    variables

    Returns:
        str: Database URI

    Raises:
        KeyError: If an environment variables has not been
            defined
    """
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")

    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")

    if not all([DB_USER, DB_PASSWORD]):
        raise MissingDatabaseCredentials()

    elif not all([provider, DB_HOST, DB_PORT, DB_NAME]):
        raise MissingDatabaseConfiguration()

    return f"{provider}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
