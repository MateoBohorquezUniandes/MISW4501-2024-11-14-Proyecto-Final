from flask import Flask, jsonify, request, Blueprint, g
from flask_jwt_extended import jwt_required, create_access_token
import os
import requests
from ..models.model import db, Usuario, UsuarioSchema
from ..errors.errors import InformacionIncompletaNoValida, InformacionIncompleta
from ..commands.crear_usuario import CrearUsuario
from ..commands.generar_token import create_token
from ..commands.db_restore import db_restore
from datetime import datetime

usuario_schema =UsuarioSchema()

usuarios_blueprint = Blueprint('usuarios', __name__)

#Consulta de salud del servicio
@usuarios_blueprint.route('/usuarios/ping', methods =['GET'])

def salud_servicio():
    return jsonify({'body':"pong"},200)


#Creación de Usuarios
@usuarios_blueprint.route('/usuarios', methods =['POST'])

def create_user():
    data = request.json
    if all (fields in data for fields in ("nombre_usuario","apellido_usuario", "tipo_identificacion", "numero_identificacion", "genero","edad", "peso","altura", "pais_nacimiento","ciudad_nacimiento", "pais_residencia", "ciudad_residencia","antiguedad_residencia","deportes_practicar","role_usuario","password")):
        command = CrearUsuario(nombre_usuario=data["nombre_usuario"], apellido_usuario=data["apellido_usuario"], 
                               tipo_identificacion=data["tipo_identificacion"], numero_identificacion=data["numero_identificacion"],
                               genero=data["genero"], edad=data["edad"],peso=data["peso"], altura=data["altura"],
                                pais_nacimiento=data["pais_nacimiento"], ciudad_nacimiento=data["ciudad_nacimiento"],
                                pais_residencia=data["pais_residencia"], ciudad_residencia=data["ciudad_residencia"],
                                antiguedad_residencia=data["antiguedad_residencia"], deportes_practicar=data["deportes_practicar"],
                                role_usuario=data["role_usuario"], password=data["password"])
        usuario = command.execute()
        token_de_acceso=create_access_token(identity=usuario.id)

        return jsonify(id=usuario.id, fechaCreacion=usuario.createdAt, token=token_de_acceso), 201
    else:
        raise InformacionIncompletaNoValida
    

#Generacion de token
@usuarios_blueprint.route('/usuarios/autenticar', methods =['POST'])
def generate_token():
    data = request.json
    if all (fields in data for fields in ("nombre_usuario","password")):

        usuario =Usuario.query.filter_by(nombre_usuario=data["nombre_usuario"]).first()

        command = create_token(nombre_usuario=data["nombre_usuario"], password=data["password"])
        result, status_code = command.execute()
        return jsonify(result), status_code
    else:
        raise InformacionIncompleta
    

#Listar Usuario en DB

@usuarios_blueprint.route('/usuarios', methods =['GET'])
@jwt_required()
def listar_usuarios():
    usuarios =Usuario.query.all()
    return [usuario_schema.dump(usuario) for usuario in usuarios]


#Restablecer base de datos  
@usuarios_blueprint.route('/usuarios/reset', methods =['POST'])
@jwt_required()
def clear_data():
    db_restore.execute()
    return jsonify({'msg':"OK"},200)
