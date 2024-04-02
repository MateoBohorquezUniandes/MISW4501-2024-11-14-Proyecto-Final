from abc import ABC, abstractmethod

from seedwork.infrastructure.schema.v1.messages import \
    IntegrationMessage


class IntegrationMapper(ABC):

    @abstractmethod
    def external_to_message(self, external: any) -> IntegrationMessage:
        raise NotImplementedError
