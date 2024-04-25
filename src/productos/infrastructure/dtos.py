from datetime import datetime
from productos.infrastructure.db import db

Base = db.declarative_base()


class Producto(db.Model):
    __tablename__ = "producto"

    id = db.Column(db.String, primary_key=True)
    tipo = db.Column(db.String())
    descripcion = db.Column(db.String())
    imagen = db.Column(db.String())
    precio = db.Column(db.Float())
    nombre = db.Column(db.String())
    deporte = db.Column(db.String())

    createdAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
    )
    updateAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
        onupdate=datetime.now,
    )
