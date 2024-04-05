from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship

from usuarios.infrastructure.db import db

Base = db.declarative_base()


class Usuario(db.Model):
    __tablename__ = "usuario"
    type = db.Column(db.String(20), nullable=True)

    # Llave compuesta, no hay necesidad de utilizar id
    tipo_identificacion = db.Column(db.String(10), primary_key=True)
    identificacion = db.Column(db.String(50), primary_key=True)
    rol = db.Column(db.String(50), primary_key=True)

    contrasena = db.Column(db.String(250), nullable=True)
    salt = db.Column(db.String(), nullable=True)

    createdAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
    )
    updateAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
        onupdate=datetime.now,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "tipo_identificacion", "identificacion", "rol", name="user_identity_unique"
        ),
    )
    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "usuario",
    }


class Deportista(Usuario):
    __tablename__ = "deportista"

    # Informacion exlusiva de deportistas
    nombre = db.Column(db.String(250), nullable=True)
    apellido = db.Column(db.String(250), nullable=True)
    #Agregando atributo planAfiliacion
    planAfiliacion = db.Column(db.String(50), primary_key=True)

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

    __mapper_args__ = {
        "polymorphic_identity": "deportista",
    }


class Organizador(Usuario):
    __tablename__ = "organizador"

    # Informacion exlusiva de deportistas
    organizacion = db.Column(db.String(250), nullable=True, unique=True)

    __mapper_args__ = {
        "polymorphic_identity": "organizador",
    }


class Socio(Usuario):
    __tablename__ = "socio"

    # Informacion exlusiva de deportistas
    razon_social = db.Column(db.String(250), nullable=True, unique=True)
    correo = db.Column(db.String(250), nullable=True)
    telefono = db.Column(db.String(250), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "socio",
    }
