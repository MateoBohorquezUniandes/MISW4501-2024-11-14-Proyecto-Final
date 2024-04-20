from flask import Flask, Response, jsonify
from flask_swagger import swagger
from flask_cors import CORS

__author__ = "Santiago Cortés Fernández"
__email__ = "s.cortes@uniandes.edu.co"


def register_handlers():
    pass


def import_alchemy_models():
    import planes.infrastructure.dtos


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

    app.secret_key = "980fa535-3542-4f74-bb11-3de3df536a76"
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["TESTING"] = config.get("TESTING")

    register_handlers()

    with app.app_context():
        from planes.infrastructure.db import db

        import_alchemy_models()

        db.init_app(app=app)
        db.create_all()

        from planes.infrastructure.auth import jwt

        jwt.init_app(app)

    from planes.presentation.commands import bp as bpc
    from planes.presentation.commands import bp_prefix as bpc_prefix
    from planes.presentation.queries import bp as bpq
    from planes.presentation.queries import bp_prefix as bpq_prefix

    app.register_blueprint(bpc, url_prefix=bpc_prefix)
    app.register_blueprint(bpq, url_prefix=bpq_prefix)

    from planes.presentation.handlers import api_custom_exception_handler
    from seedwork.presentation.exceptions import APIError

    app.register_error_handler(APIError, api_custom_exception_handler)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag["info"]["version"] = "1.0.0"
        swag["info"]["title"] = "Planes SportApp API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})

    CORS(app)

    return app
