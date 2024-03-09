from jwt_api_auth.infrastructure.db import db
from jwt_api_auth.infrastructure.dto import Usuario, UsuarioSchema


class RepositorioTokenSQLite:
    # def get_user(self, nombre_usuario:str):
    #    user = db.session.query(Usuario).filter_by(id=str(nombre_usuario)).first()
    #    return user

    def get_user(self, nombre_usuario: str):
        user = (
            db.session.query(Usuario)
            .filter_by(nombre_usuario=str(nombre_usuario))
            .first()
        )
        return UsuarioSchema().dump(user)

    def get_user_id(self, id: str):
        user = db.session.query(Usuario).filter_by(id=str(id)).first()
        return UsuarioSchema().dump(user)
