from datetime import datetime as dt

from sqlalchemy import Column, Integer, Table
from sqlalchemy.orm import declarative_base, relationship

from sesiones.infrastructure.db import db


class SesionDeportiva(db.Model):
    __tablename__ = "sesion_deportiva"

    tipo_identificacion = db.Column(db.String(10), primary_key=True)
    identificacion = db.Column(db.String(20), primary_key=True)
    id = db.Column(db.String, primary_key=True)

    exigencia = db.Column(db.String(50), nullable=False)
    deporte = db.Column(db.String(50), nullable=False)

    createdAt = db.Column(
        db.DateTime(),
        default=dt.utcnow,
    )
    completedAt = db.Column(
        db.DateTime(),
        nullable=True,
    )
    updateAt = db.Column(
        db.DateTime(),
        default=dt.utcnow,
        onupdate=dt.utcnow,
    )
