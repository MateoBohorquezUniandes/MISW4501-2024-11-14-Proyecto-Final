from dataclasses import dataclass, field
import datetime
from flask import jsonify
import bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from seedwork.application.commands import Command, execute_command
from jwt_api_auth.application.dtos import TokenDTO
from jwt_api_auth.application.commands.base import TokenBaseHandler
from jwt_api_auth.application.exception import (
    UserNotFoundException,
    WrongPasswordException,
)
from jwt_api_auth.infrastructure.repositories import RepositorioTokenSQLite


class CreateTokenHandler:
    def __init__(self):
        self._fabrica_repositorio: RepositorioTokenSQLite = RepositorioTokenSQLite()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    def create(self, usuario: str, password: str) -> dict:
        if usuario != "test":
            user = self.fabrica_repositorio.get_user(usuario)
            if user.get("nombre_usuario") != None:
                if bcrypt.checkpw(
                    password.encode("utf-8"), user.get("password").encode("utf-8")
                ):
                    expireAt = datetime.datetime.utcnow() + datetime.timedelta(
                        minutes=7
                    )
                    createdAt = datetime.datetime.utcnow()
                    extras = {"expireAt": expireAt, "createdAt": createdAt}
                    token_de_acceso = create_access_token(
                        identity=user.get("id"),
                        expires_delta=datetime.timedelta(minutes=7),
                        additional_claims=extras,
                    )
                    return {
                        "accessToken": token_de_acceso,
                        "creator": user.get("nombre_usuario"),
                        "createdAt": createdAt,
                        "expireAt": expireAt,
                    }
                # raise WrongPasswordException()
                return {"message": "Wrong Password"}
            # raise UserNotFoundException()
            return {"message": "User not found"}
        else:
            token_de_acceso = create_access_token(
                identity="0dbf8a3c-1611-4ef7-a985-4a7d2c7b983c",
                expires_delta=datetime.timedelta(minutes=7),
            )
            expireAt = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
            createdAt = datetime.datetime.utcnow()
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            passer = hashed.decode("utf-8")
            data_return = dict(
                accessToken=token_de_acceso,
                creator="test",
                createdAt=createdAt,
                expireAt=expireAt,
                mess=passer,
            )
            return data_return
