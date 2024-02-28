from usuarios.commands.base_command import BaseCommannd
from usuarios.errors.errors import InformacionEliminada
from usuarios.models.model import db


class db_restore(BaseCommannd):
    def execute():
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            print("Deleted table = {}".format(table))
            db.session.execute(table.delete())
        db.session.commit()
        raise InformacionEliminada
