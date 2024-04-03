from abc import ABC, abstractmethod


class Dispatcher(ABC):
    @abstractmethod
    def publish(self, topic):
        raise NotImplementedError

