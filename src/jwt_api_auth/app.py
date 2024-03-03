from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_swagger import swagger
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

def register_handlers():
    import jwt_api_auth.application

def import_alchemy_models():
    import jwt_api_auth.infrastructure.dto

def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)
    from jwt_api_auth.config.db import generate_database_uri
    from seedwork.infrastructure.jwt import retrieve_secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = generate_database_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = retrieve_secret_key()
    jwt = JWTManager(app)

     # Inicializa la DB
    from jwt_api_auth.config.db import init_db
    init_db(app)

    from jwt_api_auth.config.db import db
    import_alchemy_models()
    register_handlers()

    with app.app_context():
        db.create_all()

     # Importa Blueprints
    from jwt_api_auth.presentation import api

    # Registro de Blueprints
    app.register_blueprint(api.bp)

    @app.route("/health")
    def health():
        return {"status": "up"}

    return app