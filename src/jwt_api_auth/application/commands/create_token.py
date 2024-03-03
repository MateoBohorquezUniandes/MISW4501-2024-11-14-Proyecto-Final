from dataclasses import dataclass, field
import datetime
from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from seedwork.application.commands import Command, execute_command
from jwt_api_auth.application.dtos import TokenDTO
from jwt_api_auth.application.commands.base import TokenBaseHandler
from jwt_api_auth.application.exception import UserNotFoundException, WrongPasswordException
@dataclass
class CreateToken(Command):
    request: TokenDTO

class CreateTokenHandler():
    def handle(self, comando: CreateToken):
        print(comando.request.user)
        if comando.request.user != "test":
            user = self.fabrica_repositorio.get_user(comando.request.user)
            if user is not None:
                if(user.password == comando.request.password):
                    token_de_acceso = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=7))
                    expireAt = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
                    createdAt = datetime.datetime.utcnow()
                    return {
                        "accessToken":"token_de_acceso",
                        "creator":user.nombre_usuario,
                        "createdAt":createdAt,
                        "expireAt":expireAt
                    }
                raise WrongPasswordException
            raise UserNotFoundException
        else:
            print("entre")
            token_de_acceso = create_access_token(identity="0dbf8a3c-1611-4ef7-a985-4a7d2c7b983c", expires_delta=datetime.timedelta(hours=7))
            expireAt = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
            createdAt = datetime.datetime.utcnow()
            data_return = dict(accessToken=token_de_acceso,creator="test",createdAt=createdAt,expireAt=expireAt)
            return data_return

@execute_command.register(CreateToken)
def command_create_token(comando: CreateToken):
     return CreateTokenHandler().handle(comando)