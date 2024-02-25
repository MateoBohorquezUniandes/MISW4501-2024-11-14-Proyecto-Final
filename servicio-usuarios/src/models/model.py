from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, MetaData, text, Enum
from sqlalchemy.orm import declarative_base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import enum

db= SQLAlchemy()



class RoleUsuario(enum.Enum):
    DEPORTISTA=1
    ORGANIZADOR=2
    SOCIO=3

class Usuario (db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_usuario=db.Column(db.String(120), unique=True, nullable=False)
    apellido_usuario=db.Column(db.String(120))
    tipo_identificacion=db.Column(db.String(120))
    numero_identificacion=db.Column(db.String(120))
    genero=db.Column(db.String(120))
    edad=db.Column(db.String(120))
    peso=db.Column(db.String(120))
    altura=db.Column(db.String(120))
    pais_nacimiento=db.Column(db.String(120))
    ciudad_nacimiento=db.Column(db.String(120))
    pais_residencia=db.Column(db.String(120))
    ciudad_residencia=db.Column(db.String(120))
    antiguedad_residencia=db.Column(db.String(120))
    deportes_practicar=db.Column(db.String(120))
    role_usuario=db.Column(db.Enum(RoleUsuario))
    password=db.Column(db.String(150))
    #token = db.Column(db.String(120), unique=True)
    createdAt=db.Column(db.DateTime, default=datetime.utcnow)
    updateAt=db.Column(db.DateTime, onupdate=datetime.utcnow)
    expireAt=db.Column(db.DateTime, default=datetime.utcnow)


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {'llave': value.name, 'valor': value.value}

class UsuarioSchema(SQLAlchemyAutoSchema):
    id = fields.String()
    nombre_usuario = fields.String()
    apellido_usuario = fields.String()
    tipo_identificacion = fields.String()
    numero_identificacion = fields.String()
    genero = fields.String()
    edad = fields.String()
    peso = fields.String()
    altura = fields.String()
    pais_nacimiento = fields.String()
    ciudad_nacimiento = fields.String()
    pais_residencia = fields.String()
    ciudad_residencia = fields.String()
    antiguedad_residencia = fields.String()
    deportes_practicar = fields.String()
    role_usuario = EnumADiccionario(attribute='role_usuario')
    password = fields.String()
    token = fields.String()
    createdAt = fields.String()
    updateAt = fields.String()
    expireAt = fields.String()

    class Meta:
        model = Usuario
        load_instance = True

    data = fields.Raw(load_only=True)