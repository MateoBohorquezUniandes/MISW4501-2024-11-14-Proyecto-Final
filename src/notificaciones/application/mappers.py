from notificaciones.application.dtos import SendToTopicDTO, SubscribeToTopicDTO
from seedwork.application.dtos import Mapper as ApplicationMapper
from seedwork.domain.repositories import Mapper as DomainMapper

# #####################################################################################
# Application Mappers
# #####################################################################################


class SendToTopicDTODictMapper(ApplicationMapper):
    def external_to_dto(self, external: dict) -> SendToTopicDTO:

        return SendToTopicDTO(
            topico=external.get("topic", ""),
            titulo=external.get("titulo", ""),
            cuerpo=external.get("body", ""),
        )

    def dto_to_external(self, dto: SendToTopicDTO) -> dict:
        return dto.__dict__


class SubscribeToTopicDTODictMapper(ApplicationMapper):
    def external_to_dto(self, external: dict) -> SubscribeToTopicDTO:

        return SubscribeToTopicDTO(
            topico=external.get("topic", ""),
            tokens=external.get("registration_tokens", ""),
        )

    def dto_to_external(self, dto: SubscribeToTopicDTO) -> dict:
        return dto.__dict__
