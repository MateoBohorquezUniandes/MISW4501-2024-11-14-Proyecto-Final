from abc import ABC, abstractmethod


class HTTPService(ABC):
    @abstractmethod
    def request(self, *args, **kwargs):
        raise NotImplementedError