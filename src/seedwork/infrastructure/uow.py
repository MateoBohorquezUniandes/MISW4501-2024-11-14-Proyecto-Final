import pickle
from abc import ABC, abstractmethod
from enum import Enum

from pydispatch import dispatcher
from seedwork.domain.entities import RootAggregation


class Lock(Enum):
    POSITIVE = 1
    PESIMIST = 2


class Batch:
    def __init__(self, process, lock: Lock, *args, **kwargs):
        self.process = process
        self.args = args
        self.lock = lock
        self.kwargs = kwargs


class UnitOfWork(ABC):

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def _fetch_events(self, batches=None):
        batches = self.batches if batches is None else batches
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, RootAggregation):
                    return arg.events
        return list()

    @abstractmethod
    def _clear_batches(self):
        raise NotImplementedError

    @abstractmethod
    def batches(self) -> list[Batch]:
        raise NotImplementedError

    @abstractmethod
    def savepoint(self):
        raise NotImplementedError

    @abstractmethod
    def savepoints(self) -> list:
        raise NotImplementedError

    def commit(self):
        self._publish_events_post_commit()
        self._clear_batches()

    @abstractmethod
    def rollback(self, savepoint=None):
        self._clear_batches()

    def register_batch(self, operacion, *args, lock=Lock.PESIMIST, **kwargs):
        batch = Batch(operacion, lock, *args, **kwargs)
        self.batches.append(batch)
        self._publish_domain_events(batch)

    def _publish_domain_events(self, batch):
        for event in self._fetch_events(batches=[batch]):
            dispatcher.send(signal=f"{type(event).__name__}Domain", event=event)

    def _publish_events_post_commit(self):
        for event in self._fetch_events():
            dispatcher.send(signal=f"{type(event).__name__}Integration", event=event)


class UnitOfWorkFactory(ABC):

    @abstractmethod
    def register_unit_of_work(self, serialized_uwo):
        raise NotImplementedError

    @abstractmethod
    def unit_of_work(self) -> UnitOfWork:
        raise NotImplementedError

    @abstractmethod
    def store_unit_of_work(self, uow: UnitOfWork):
        raise NotImplementedError


class UnitOfWorkPort:

    @staticmethod
    def commit(uowf: UnitOfWorkFactory):
        uow = uowf.unit_of_work()
        uow.commit()
        uowf.store_unit_of_work(uow)

    @staticmethod
    def rollback(uowf: UnitOfWorkFactory, savepoint=None):
        uow = uowf.unit_of_work()
        uow.rollback(savepoint=savepoint)
        uowf.store_unit_of_work(uow)

    @staticmethod
    def savepoint(uowf: UnitOfWorkFactory):
        uow = uowf.unit_of_work()
        uow.savepoint()
        uowf.store_unit_of_work(uow)

    @staticmethod
    def fetch_savepoints(uowf: UnitOfWorkFactory):
        uow = uowf.unit_of_work()
        return uow.savepoints()

    @staticmethod
    def register_batch(
        uowf: UnitOfWorkFactory, operacion, *args, lock=Lock.PESIMIST, **kwargs
    ):
        uow = uowf.unit_of_work()
        uow.register_batch(operacion, *args, lock=lock, **kwargs)
        uowf.store_unit_of_work(uow)
