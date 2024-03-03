from .base_command import BaseCommannd
from flask_jwt_extended import jwt_required, create_access_token
#Pendiente configurar los errores
from ..models.model import Usuario
from ..models.model import db
from ..models.model import RoleUsuario
from ..errors.errors import InformacionIncompletaNoValida
from ..errors.errors import CaractersEspeciales
from ..errors.errors import EspacioenNombreUsuario
from ..errors.errors import FormatoInvalidoID
from ..errors.errors import UsuarioyaExiste
from ..commands.utils import set_password
from ..commands.generar_token import create_token
import datetime
import uuid
import os
import re

class CrearUsuario(BaseCommannd):
    def __init__ (self,nombre_usuario, apellido_usuario, tipo_identificacion,numero_identificacion, genero, edad, peso, altura, pais_nacimiento, ciudad_nacimiento, pais_residencia, ciudad_residencia,antiguedad_residencia,deportes_practicar,role_usuario, password):
        self.nombre_usuario= nombre_usuario
        self.apellido_usuario=apellido_usuario
        self.tipo_identificacion= tipo_identificacion
        self.numero_identificacion= numero_identificacion
        self.genero=genero
        self.edad= edad
        self.peso=peso
        self.altura=altura
        self.pais_nacimiento=pais_nacimiento
        self.ciudad_nacimiento=ciudad_nacimiento
        self.pais_residencia=pais_residencia
        self.ciudad_residencia=ciudad_residencia
        self.antiguedad_residencia=antiguedad_residencia
        self.deportes_practicar=deportes_practicar
        self.role_usuario=role_usuario
        self.password=password
        self.createdAt=datetime.datetime.utcnow()
        self.updateAt=datetime.datetime.utcnow()
        self.expireAt=datetime.datetime.utcnow()
 
    def execute(self):

        #Definir campos mandatorios
        if not all ([self.nombre_usuario,self.apellido_usuario,self.numero_identificacion]):
           raise InformacionIncompletaNoValida
        
        ##Se comentan estas validaciones para pruebas en JMeter
        
        # #Validar que el nombre no tiene caracteres especiales
        # regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

        # if(regex.search(self.nombre_usuario) != None):
        #     raise CaractersEspeciales
        
        # if " " in self.nombre_usuario:
        #     raise EspacioenNombreUsuario

        # #Validar que el ID es ingresado en números   
        # if len(self.numero_identificacion)>1:
        #     if not (self.numero_identificacion.isnumeric()):
        #         raise FormatoInvalidoID


        # if Usuario.query.filter_by(nombre_usuario=self.nombre_usuario).first() or Usuario.query.filter_by(numero_identificacion=self.numero_identificacion).first():
        #     raise UsuarioyaExiste
        
        # password hashed
        hashed_password = set_password(self.password)
        
        
        usuario =Usuario(nombre_usuario=self.nombre_usuario, apellido_usuario=self.apellido_usuario,
                          tipo_identificacion=self.tipo_identificacion, numero_identificacion=self.numero_identificacion, 
                          genero=self.genero, edad = self.edad,peso=self.peso, altura=self.altura, 
                          pais_nacimiento=self.pais_nacimiento, ciudad_nacimiento=self.ciudad_nacimiento, 
                          pais_residencia=self.pais_residencia, ciudad_residencia=self.ciudad_residencia, 
                          antiguedad_residencia=self.antiguedad_residencia, deportes_practicar=self.deportes_practicar, 
                          role_usuario=self.role_usuario, password=hashed_password, 
                          createdAt=self.createdAt,updateAt=self.updateAt)   

        usuario.expireAt= datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        db.session.add(usuario)
        db.session.commit()

        return usuario