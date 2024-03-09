import os
from hashlib import md5
import json
import random
from flask import Flask, jsonify, Response
from flask_swagger import swagger

from perfiles.presentation.handlers import api_custom_exception_handler
from seedwork.presentation.exceptions import APIError

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
    from seedwork.infrastructure.jwt import retrieve_secret_key

    db_provider = config.get("database_provider", "postgresql")
    app.config["SQLALCHEMY_DATABASE_URI"] = generate_database_uri(db_provider)
    app.config["JWT_SECRET_KEY"] = retrieve_secret_key()

    with app.app_context():
        from perfiles.infrastructure.db import db

        db.init_app(app=app)
        db.create_all()

        from perfiles.infrastructure.jwt import jwt

        jwt.init_app(app)

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
        return jsonify({"status": "healthy"})
    
    @app.route("/health-test")
    def health_test():
        return jsonify({"status": "healthy"})

    @app.after_request
    def after_request(response: Response):
        fail_rate = float(os.environ["FAIL_RATE"])
        r = random.random()
        check_input = response.json if r <= fail_rate else {"data": "fake"}
        
        data = dict(
            data=response.json,
            checksum=md5(
                json.dumps(check_input, sort_keys=True).encode("utf-8")
            ).hexdigest(),
        )
        response.set_data(json.dumps(data))
        return response

    return app
