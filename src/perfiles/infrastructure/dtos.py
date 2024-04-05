from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship

from perfiles.infrastructure.db import db


class PerfilDemografico(db.Model):
    __tablename__ = "perfil_demografico"

    tipo_identificacion = db.Column(db.String(10), primary_key=True)
    identificacion = db.Column(db.String(20), primary_key=True)

    pais = db.Column(db.String(120), nullable=True)
    ciudad = db.Column(db.String(120), nullable=True)

    genero = db.Column(db.String(10), nullable=True)
    edad = db.Column(db.Integer, nullable=True)
    peso = db.Column(db.Float, nullable=True)
    altura = db.Column(db.Float, nullable=True)

    imc_valor = db.Column(db.Float, nullable=True)
    imc_cateroria = db.Column(db.String(50))
    clasificacion_riesgo = db.Column(db.String(50))

    reportes_sanguineos = relationship("ReporteSanguineo", backref="perfil_demografico")


class ReporteSanguineo(db.Model):
    __tablename__ = "reporte_sanguineo"

    tipo_examen = db.Column(db.String(20), primary_key=True)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow(), primary_key=True)

    tipo_identificacion = db.Column(db.String(10), nullable=False)
    identificacion = db.Column(db.String(20), nullable=False)

    valor = db.Column(db.Float(), nullable=False)
    unidad = db.Column(db.String(10), nullable=False)

    __table_args__ = (
        db.ForeignKeyConstraint(
            [tipo_identificacion, identificacion],
            [
                PerfilDemografico.tipo_identificacion,
                PerfilDemografico.identificacion,
            ],
        ),
    )


class PerfilDeportivo(db.Model):
    __tablename__ = "perfil_deportivo"

    tipo_identificacion = db.Column(db.String(10), primary_key=True)
    identificacion = db.Column(db.String(20), primary_key=True)


class PerfilAlimenticio(db.Model):
    __tablename__ = "perfil_alimenticio"

    tipo_identificacion = db.Column(db.String(10), primary_key=True)
    identificacion = db.Column(db.String(20), primary_key=True)
