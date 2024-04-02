from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship

from usuarios.infrastructure.db import db

Base = db.declarative_base()

class Usuario(db.Model):
    # Llave compuesta, no hay necesidad de utilizar id
    tipo_identificacion = db.Column(db.String(10), primary_key=True)
    identificacion = db.Column(db.String(50), primary_key=True)
    rol = db.Column(db.String(50), primary_key=True)

    contrasena = db.Column(db.String(250), nullable=False)
    salt = db.Column(db.String(), nullable=False)

    nombre = db.Column(db.String(250), nullable=False)
    apellido = db.Column(db.String(250), nullable=False)

    # Informacion exlusiva de deportistas
    genero = db.Column(db.String(10), nullable=True)
    edad = db.Column(db.Integer, nullable=True)
    peso = db.Column(db.Float, nullable=True)
    altura = db.Column(db.Float, nullable=True)

    pais_nacimiento = db.Column(db.String(120), nullable=True)
    ciudad_nacimiento = db.Column(db.String(120), nullable=True)

    pais_residencia = db.Column(db.String(120), nullable=True)
    ciudad_residencia = db.Column(db.String(120), nullable=True)
    tiempo_residencia = db.Column(db.Integer, nullable=True)

    deportes = db.Column(db.String, nullable=True)

    createdAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
    )
    updateAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
        onupdate=datetime.now,
    )

    __table_args__ = (db.UniqueConstraint("tipo_identificacion", "identificacion", name="user_identity_unique"),)
