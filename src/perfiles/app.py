from flask import Flask, jsonify
from flask_swagger import swagger
from marshmallow import ValidationError

from seedwork.presentation.exceptions import APIError
from perfiles.presentation.handlers import api_custom_exception_handler

__author__ = "Santiago Cortés Fernández"
__email__ = "s.cortes@uniandes.edu.co"


def create_app(config={}):
    """
    Factory function for generating a new application

    Returns:
        flask.Flask: application instance
    """
    app = Flask(__name__, instance_relative_config=True)

    from seedwork.infrastructure.db import generate_database_uri

    db_provider = config.get("database_provider", "postgresql")
    app.config["SQLALCHEMY_DATABASE_URI"] = generate_database_uri(db_provider)

    with app.app_context():
        from perfiles.infrastructure.db import db

        db.init_app(app=app)
        db.create_all()

    from perfiles.presentation.api import bp, bp_prefix

    app.register_blueprint(bp, url_prefix=bp_prefix)

    app.register_error_handler(APIError, api_custom_exception_handler)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag["info"]["version"] = "1.0.0"
        swag["info"]["title"] = "Perfiles SportApp API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "healthy"}

    return app