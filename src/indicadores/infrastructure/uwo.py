import pickle

from indicadores.infrastructure.db import db
from seedwork.infrastructure.uow import Batch, Lock, UnitOfWork, UnitOfWorkFactory


class UnitOfWorkSQLAlchemy(UnitOfWork):

    def __init__(self):
        self._batches: list[Batch] = list()

    def __enter__(self) -> UnitOfWork:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def _clear_batches(self):
        self._batches = list()

    @property
    def batches(self) -> list[Batch]:
        return self._batches

    @property
    def savepoints(self) -> list:
        return list[db.session.get_nested_transaction()]

    def commit(self):
        if any([b.process is not None for b in self.batches]):
            for batch in self.batches:
                lock = batch.lock
                batch.process(*batch.args, **batch.kwargs)
            db.session.commit()

        super().commit()

    def rollback(self, savepoint=None):
        if savepoint:
            savepoint.rollback()
        else:
            db.session.rollback()

        super().rollback()

    def savepoint(self):
        db.session.begin_nested()


class UnitOfWorkASQLAlchemyFactory(UnitOfWorkFactory):

    def register_unit_of_work(self, serialized_obj):
        from flask import session

        session["uow"] = serialized_obj

    def unit_of_work(self) -> UnitOfWork:
        if self._is_flask():
            return pickle.loads(self._flask_uow())
        else:
            raise Exception("No hay unidad de trabajo")

    def store_unit_of_work(self, uow: UnitOfWork):
        if self._is_flask():
            self.register_unit_of_work(pickle.dumps(uow))
        else:
            raise Exception("No hay unidad de trabajo")

    def _is_flask(self):
        try:
            from flask import session

            return True
        except Exception as e:
            return False

    def _flask_uow(self):
        from flask import session

        if session.get("uow"):
            return session["uow"]
        else:
            uow_serialized = pickle.dumps(UnitOfWorkSQLAlchemy())
            self.register_unit_of_work(uow_serialized)
            return uow_serialized
