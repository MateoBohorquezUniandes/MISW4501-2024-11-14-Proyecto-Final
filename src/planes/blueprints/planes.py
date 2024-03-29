from flask import Blueprint, Flask, g, jsonify, request
from flask_jwt_extended import jwt_required

import seedwork.presentation.api as api
from planes.commands.db_restore import db_restore
from planes.commands.crear_planDeportivo import CrearPlanDeportivo
from planes.errors.errors import InformacionIncompletaNoValida
from planes.models.model import PlanDeportivo, PlanDeportivoSchema, db

import requests
import os

bp_prefix: str = "/planes"
bp: Blueprint = api.create_blueprint("planes", bp_prefix)

bp = Blueprint("planes", __name__)

#base_url = os.environ["JWt_BASE_URL"]
#JWT_VALIDATE_URL = f"{base_url}/validate"
plan_deportivo_schema=PlanDeportivoSchema()


#Consulta de salud del servicio Planes
@bp.route('/ping', methods =['GET'])
def service_health():
    return jsonify({'body':"pong"},200)

#Crear Plan
@bp.route('/', methods =['POST'])
def create_plan():
    data = request.json
    if all (fields in data for fields in ("nombrePlan", "nivelExigencia")):
        command = CrearPlanDeportivo(nombrePlan=data["nombrePlan"], nivelExigencia=data["nivelExigencia"])
        planDeportivo=command.execute()

        #return (
           # jsonify(id=planDeportivo.id, nombrePlan=planDeportivo.nombrePlan, nivelExigencia=planDeportivo.nivelExigencia),
           # 201,
        #)
        return plan_deportivo_schema.dump(planDeportivo)
    else:
        raise InformacionIncompletaNoValida

#Obtener todos los planes deportivos
@bp.route("/", methods=["GET"])
def listar_planes():
    planesDeportivos = PlanDeportivo.query.all()
    return [plan_deportivo_schema.dump(plan) for plan in planesDeportivos]   

#Reset DB

@bp.route("/reset", methods=["DELETE"])
@jwt_required()
def clear_data():
    db_restore.execute()
    return jsonify({"msg": "OK"}, 200)


