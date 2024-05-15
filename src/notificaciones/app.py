from flask import Flask, Response, jsonify
from flask_swagger import swagger
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials

def register_handlers():
    pass

def create_app(config={}):
    """
    Factory function for generating a new application

    Returns:
        flask.Flask: application instance
    """
    app = Flask(__name__, instance_relative_config=True)

    from seedwork.infrastructure.db import generate_database_uri
    from seedwork.infrastructure.jwt import retrieve_secret_key

    app.secret_key = "97eea083-fea7-4b2b-9765-a5cc7d7a411c"
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["TESTING"] = config.get("TESTING")

    register_handlers()

    with app.app_context():
        from notificaciones.infrastructure.db import db

        from notificaciones.infrastructure.auth import jwt

        jwt.init_app(app)

    app_options = {"projectId": "proyecto-final-416123"}

    firebase_admin.initialize_app(options=app_options)
    from notificaciones.presentation.commands import bp as bpc, bp_prefix as bpc_prefix

    app.register_blueprint(bpc, url_prefix=bpc_prefix)

    from seedwork.presentation.exceptions import APIError
    from notificaciones.presentation.handlers import api_custom_exception_handler

    app.register_error_handler(APIError, api_custom_exception_handler)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag["info"]["version"] = "1.0.0"
        swag["info"]["title"] = "Autenticador SportApp API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})

    CORS(app)

    return app
