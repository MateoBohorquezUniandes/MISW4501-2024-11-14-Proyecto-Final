from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship

from planes.infrastructure.db import db

Base = db.declarative_base()


recomendacion_table = db.Table(
    "recomendaciones",
    db.Model.metadata,
    db.Column("usuario_id", db.ForeignKey("usuario_plan.id"), primary_key=True),
    db.Column("plan_id", db.ForeignKey("plan_entrenamiento.id"), primary_key=True),
)


class UsuarioPlan(db.Model):
    __tablename__ = "usuario_plan"

    id = db.Column(db.String, primary_key=True)
    tipo_identificacion = db.Column(db.String(10), nullable=False)
    identificacion = db.Column(db.String(20), nullable=False)

    createdAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
    )
    updateAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
        onupdate=datetime.now,
    )

    planes = db.relationship(
        "PlanEntrenamiento",
        secondary=recomendacion_table,
        back_populates="usuarios",
        lazy="select",
    )

    __table_args__ = (
        db.UniqueConstraint(
            "tipo_identificacion", "identificacion", name="usuario_plan_identity_unique"
        ),
    )


class Entrenamiento(db.Model):
    __tablename__ = "entrenamiento"

    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)

    grupo_muscular = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(400), nullable=False)
    imagen = db.Column(db.String(400), nullable=True)

    duracion = db.Column(db.Integer, nullable=False)
    duracion_unidad = db.Column(db.String(50), nullable=False)
    series = db.Column(db.Integer, nullable=False)

    plan_id = db.Column(db.String, db.ForeignKey("plan_entrenamiento.id"))

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
            "plan_id",
            "nombre",
            "grupo_muscular",
            "duracion",
            "duracion_unidad",
            "series",
            name="entrenamiento_unique",
        ),
    )


class PlanEntrenamiento(db.Model):
    __tablename__ = "plan_entrenamiento"

    id = db.Column(db.String, primary_key=True)

    nombre = db.Column(db.String(120), nullable=False, unique=True)
    categoria = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(400), nullable=False)

    nivel_exigencia = db.Column(db.String(50), nullable=False)
    deporte_objetivo = db.Column(db.String(50), nullable=False)

    entrenamientos = db.relationship(
        Entrenamiento, cascade="all,delete", backref="plan"
    )

    usuarios = db.relationship(
        "UsuarioPlan",
        secondary=recomendacion_table,
        back_populates="planes",
        lazy="dynamic",
    )

    createdAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
    )
    updateAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
        onupdate=datetime.now,
    )


class RutinaRecuperacion(db.Model):
    __tablename__ = "rutina_recuperacion"

    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)

    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(400), nullable=False)
    imagen = db.Column(db.String(400), nullable=True)

    duracion = db.Column(db.Integer, nullable=False)
    duracion_unidad = db.Column(db.String(50), nullable=False)

    frecuencia = db.Column(db.Integer, nullable=False)
    frecuencia_unidad = db.Column(db.String(50), nullable=False)

    createdAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
    )
    updateAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
        onupdate=datetime.now,
    )


class GrupoAlimenticio(db.Model):
    __tablename__ = "grupo_alimenticio"

    id = db.Column(db.String, primary_key=True)
    grupo = db.Column(db.String(120), nullable=False)

    porcion = db.Column(db.Float, nullable=False)
    porcion_unidad = db.Column(db.String(50), nullable=False)
    calorias = db.Column(db.Float, nullable=False)

    rutina_id = db.Column(db.String, db.ForeignKey("rutina_alimentacion.id"))

    createdAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
    )
    updateAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
        onupdate=datetime.now,
    )


class RutinaAlimentacion(db.Model):
    __tablename__ = "rutina_alimentacion"

    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)

    descripcion = db.Column(db.String(400), nullable=False)
    imagen = db.Column(db.String(400), nullable=True)
    tipo_alimentacion = db.Column(db.String(), nullable=False)
    deporte = db.Column(db.String(), nullable=False)

    grupos_alimenticios = db.relationship(
        GrupoAlimenticio, cascade="all,delete", backref="rutina"
    )

    createdAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
    )
    updateAt = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
        onupdate=datetime.now,
    )
