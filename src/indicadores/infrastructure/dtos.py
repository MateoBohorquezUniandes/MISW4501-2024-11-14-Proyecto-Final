from datetime import datetime as dt

from sqlalchemy import Column, Integer, Table
from sqlalchemy.orm import declarative_base, relationship

from indicadores.infrastructure.db import db

TIPO_GLOBAL = "global"
IDENTIFICACION_GLOBAL = "global"

class Formula(db.Model):
    __tablename__ = "formula"

    id = db.Column(db.String, primary_key=True)
    tipo_identificacion = db.Column(db.String(10), nullable=False)
    identificacion = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)
    formula = db.Column(db.String(100), nullable=False)
    parametros = db.relationship('Parametro', backref='parametro')


class Indicador(db.Model):
    __tablename__ = "indicador"

    idSesion = db.Column(db.String, primary_key=True)
    idFormula = db.Column(db.String(20), nullable=False)
    valor = db.Column(db.String(10), nullable=False)
    varianza = db.Column(db.String(10), nullable=False)

class Parametro(db.Model):
    __tablename__ = "parametro"

    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    simbolo = db.Column(db.String(1), nullable=False)
    funcion = db.Column(db.String(3), nullable=False)
    id_formula = db.Column(db.String, db.ForeignKey("formula.id"))
