import uuid

from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from eventos.infrastructure.db import db

Base = db.declarative_base()


class Evento(db.Model):
    __tablename__ = "evento"

    id = db.Column(db.String, primary_key=True)
    tipo = db.Column(db.String(20))
    fecha = db.Column(db.DateTime())
    lugar = db.Column(db.String(20))
    distancia = db.Column(db.Float())
    nivel = db.Column(db.String(20))

    createdAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
    )
    updateAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
        onupdate=datetime.now,
    )
