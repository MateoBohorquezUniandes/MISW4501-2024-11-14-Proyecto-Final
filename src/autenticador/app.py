from flask import Flask, Response, jsonify
from flask_swagger import swagger


def register_handlers():
    import autenticador.application


def create_app(config={}):
    """
    Factory function for generating a new application

    Returns:
        flask.Flask: application instance
    """
    app = Flask(__name__, instance_relative_config=True)

    from seedwork.infrastructure.jwt import retrieve_secret_key

    app.config["JWT_SECRET_KEY"] = retrieve_secret_key()

    app.secret_key = "9d58f98f-3ae8-4149-a09f-3a8c2012e32c"
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["TESTING"] = config.get("TESTING")

    register_handlers()

    with app.app_context():
        from autenticador.infrastructure.auth import jwt

        jwt.init_app(app)

    from autenticador.presentation.api import bp, bp_prefix

    app.register_blueprint(bp, url_prefix=bp_prefix)

    from seedwork.presentation.exceptions import APIError
    from autenticador.presentation.handlers import api_custom_exception_handler

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

    return app
