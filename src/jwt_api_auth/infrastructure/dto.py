from jwt_api_auth.config.db import db
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, Table
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, Schema

import enum
import uuid
from datetime import datetime

Base = db.declarative_base()

class RoleUsuario(enum.Enum):
    DEPORTISTA = 1
    ORGANIZADOR = 2
    SOCIO = 3

class Usuario(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_usuario = db.Column(db.String(120), nullable=False)
    apellido_usuario = db.Column(db.String(120))
    tipo_identificacion = db.Column(db.String(120))
    numero_identificacion = db.Column(db.String(120))
    genero = db.Column(db.String(120))
    edad = db.Column(db.String(120))
    peso = db.Column(db.String(120))
    altura = db.Column(db.String(120))
    pais_nacimiento = db.Column(db.String(120))
    ciudad_nacimiento = db.Column(db.String(120))
    pais_residencia = db.Column(db.String(120))
    ciudad_residencia = db.Column(db.String(120))
    antiguedad_residencia = db.Column(db.String(120))
    deportes_practicar = db.Column(db.String(120))
    role_usuario = db.Column(db.Enum(RoleUsuario))
    password = db.Column(db.String(150))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updateAt = db.Column(db.DateTime, onupdate=datetime.utcnow)
    expireAt = db.Column(db.DateTime, default=datetime.utcnow)

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        include_fk = True
        load_instance = True
        
    id = fields.String()
    nombre_usuario = fields.String()
    password = fields.String()
    role_usuario = fields.String()