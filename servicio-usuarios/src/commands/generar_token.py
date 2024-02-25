from .base_command import BaseCommannd
from flask_jwt_extended import jwt_required, create_access_token
from .utils import set_password, check_password
import uuid, datetime
from ..models.model import Usuario, db
from ..errors.errors import UsuariooContrasenaIncorrectos, InformacionIncompleta

class create_token(BaseCommannd):

    def __init__ (self, nombre_usuario,password=None, nuevo_usuario=False):
        self.nombre_usuario= nombre_usuario
        self.password=password
        self.nuevo_usuario = nuevo_usuario
        self.id=""
        self.token=""
        self.expireAt =""
  

    def execute(self):
        usuario = Usuario.query.filter_by(nombre_usuario=self.nombre_usuario).first()

        if self.password:
            if not usuario or not check_password(usuario.password, self.password):
                raise UsuariooContrasenaIncorrectos

        else:
            # Excepcion cuando no se define el parametro nuevo_usuario o la contraseña 
            raise InformacionIncompleta

        # Generate the token
        token_de_acceso=create_access_token(identity=usuario.id)
        usuario.expireAt= datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        # Save the token in the database
        db.session.add(usuario)
        db.session.commit()

        return {
            'id': usuario.id,
            'token': token_de_acceso,
            'expireAt': usuario.expireAt
        }, 200
