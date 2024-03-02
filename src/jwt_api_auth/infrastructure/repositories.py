from jwt_api_auth.config.db import db
from jwt_api_auth.infrastructure.dto import Usuario

class RepositorioTokenSQLite():
    def get_user(self, nombre_usuario:str):
        user = db.session.query(Usuario).filter_by(id=str(nombre_usuario)).one()
        return user