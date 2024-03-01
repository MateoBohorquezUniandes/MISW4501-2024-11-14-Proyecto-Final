from flask import Flask, jsonify
from flask_swagger import swagger

from usuarios.errors.errors import ApiError


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
        from usuarios.models.model import db

        db.init_app(app=app)
        db.create_all()

        from usuarios.infrastructure.jwt import jwt

        jwt.init_app(app)

    from usuarios.blueprints.usuarios import bp, bp_prefix

    app.register_blueprint(bp, url_prefix=bp_prefix)

    def handle_exception(err):
        response = {
            "msg": err.description,
            # "version": os.environ["VERSION"]
        }
        return jsonify(response), err.code

    app.register_error_handler(ApiError, handle_exception)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag["info"]["version"] = "1.0.0"
        swag["info"]["title"] = "Usuarios SportApp API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "healthy"}

    return app
