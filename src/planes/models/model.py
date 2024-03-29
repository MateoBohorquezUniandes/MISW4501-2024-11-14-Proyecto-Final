from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import uuid
from datetime import datetime
import enum

db = SQLAlchemy()

class NivelExigencia(enum.Enum):
    ALTO = 1
    MEDIO = 2
    BAJO = 3

class PlanDeportivo(db.Model):
    #id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id = db.Column(db.Integer, primary_key=True)
    nombrePlan = db.Column(db.String)
    nivelExigencia = db.Column(db.Enum(NivelExigencia))
    #userId = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    userId= db.Column(db.String)

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class PlanDeportivoSchema(SQLAlchemyAutoSchema):
    id = fields.String()
    nombrePlan = fields.String()
    nivelExigencia = EnumADiccionario(attribute="nivelExigencia")

    class Meta:
        model = PlanDeportivo
        load_instance = True
        include_relationships = True
        include_fk = True

    data = fields.Raw(load_only=True)
