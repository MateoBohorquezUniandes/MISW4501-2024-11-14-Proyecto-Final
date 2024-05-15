from dataclasses import dataclass, field
import traceback
from notificaciones.application.commands.base import NotificacionesCommandBaseHandler
from notificaciones.application.dtos import SubscribeToTopicDTO
from notificaciones.application.exceptions import UnprocessableEntityError
from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError


@dataclass
class SubscribeToTopic(Command):
    message_dto: SubscribeToTopicDTO = field(default_factory=SubscribeToTopicDTO)


class SubscribeToTopicHandler(NotificacionesCommandBaseHandler):
    def handle(self, command: SubscribeToTopic):
        try:
            message_dto = command.message_dto
            self.message_admin.subscribe_topic(message_dto.tokens, message_dto.topico)
        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)

        except Exception as e:
            traceback.print_exc()

            raise APIError(message=str(e), code="notificaciones.error.internal")


@execute_command.register(SubscribeToTopic)
def command_send_to_topic(command: SubscribeToTopic):
    SubscribeToTopicHandler().handle(command)
