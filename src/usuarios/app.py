import os

from flask import Flask, Response, jsonify
from flask_swagger import swagger
from flask_cors import CORS

__author__ = "Santiago Cortés Fernández"
__email__ = "s.cortes@uniandes.edu.co"


def register_handlers():
    import usuarios.application


def import_alchemy_models():
    import usuarios.infrastructure.dtos


def create_app(config={}):
    """
    Factory function for generating a new application

    Returns:
        flask.Flask: application instance
    """
    app = Flask(__name__, instance_relative_config=True)

    from seedwork.infrastructure.db import generate_database_uri
    from seedwork.infrastructure.jwt import retrieve_secret_key

    db_provider = config.get("database_provider", "postgresql")
    app.config["SQLALCHEMY_DATABASE_URI"] = generate_database_uri(db_provider)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = retrieve_secret_key()

    app.secret_key = "9d58f98f-3ae8-4149-a09f-3a8c2012e32c"
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["TESTING"] = config.get("TESTING")

    register_handlers()

    with app.app_context():
        from usuarios.infrastructure.db import db

        import_alchemy_models()

        db.init_app(app=app)
        db.create_all()

        from usuarios.infrastructure.auth import jwt

        jwt.init_app(app)

    from usuarios.presentation.commands import bp as bpc
    from usuarios.presentation.commands import bp_prefix as bpc_prefix

    app.register_blueprint(bpc, url_prefix=bpc_prefix)

    from seedwork.presentation.exceptions import APIError
    from usuarios.presentation.handlers import api_custom_exception_handler

    app.register_error_handler(APIError, api_custom_exception_handler)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag["info"]["version"] = "1.0.0"
        swag["info"]["title"] = "Usuarios SportApp API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})
    
    origins = os.environ.get("ORIGINS")
    CORS(app, origins=[origins])

    return app
