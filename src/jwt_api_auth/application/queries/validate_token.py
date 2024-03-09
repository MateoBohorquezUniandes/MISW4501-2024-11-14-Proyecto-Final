from dataclasses import dataclass, field
import datetime
from flask import jsonify
from flask_jwt_extended import decode_token
from flask_jwt_extended import JWTManager
from seedwork.application.commands import Command, execute_command
from jwt_api_auth.application.dtos import TokenDTO
from jwt_api_auth.application.commands.base import TokenBaseHandler
from jwt_api_auth.application.exception import (
    UserNotFoundException,
    WrongPasswordException,
)
from jwt_api_auth.infrastructure.repositories import RepositorioTokenSQLite


class ValidateTokenHandler:
    def __init__(self):
        self._fabrica_repositorio: RepositorioTokenSQLite = RepositorioTokenSQLite()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    def create(self, accessToken: str) -> dict:
        data_decode = decode_token(accessToken, allow_expired=True)
        fecha_expira = datetime.datetime.strptime(
            data_decode.get("expireAt"), "%a, %d %b %Y %H:%M:%S %Z"
        )
        if fecha_expira < datetime.datetime.now():
            retorno = {
                "accessToken": accessToken,
                "isValid": False,
                "message": "Token Expired",
            }
            return retorno
        else:
            user = self.fabrica_repositorio.get_user_id(data_decode.get("sub"))
            if user.get("nombre_usuario") == None:
                retorno = {
                    "accessToken": accessToken,
                    "isValid": False,
                    "message": "User not found",
                }
                return retorno
            else:
                retorno = {
                    "accessToken": accessToken,
                    "isValid": True,
                    "message": {"user": user.get("nombre_usuario")},
                }
                return retorno
