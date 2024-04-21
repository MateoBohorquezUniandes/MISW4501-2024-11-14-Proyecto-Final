from datetime import datetime as dt

from sqlalchemy import Column, Integer, Table
from sqlalchemy.orm import declarative_base, relationship

from productos.infrastructure.db import db

class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String(20), primary_key=True)
    precio = db.Column(db.String(10), primary_key=True)
    tipo = db.Column(db.String(20), primary_key=True)