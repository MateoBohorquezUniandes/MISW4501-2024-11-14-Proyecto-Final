from dataclasses import dataclass, field
import traceback
from notificaciones.application.commands.base import NotificacionesCommandBaseHandler
from notificaciones.application.dtos import SendToTopicDTO
from notificaciones.application.exceptions import UnprocessableEntityError
from seedwork.application.commands import Command, execute_command
from seedwork.domain.exceptions import BusinessRuleException
from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.presentation.exceptions import APIError


@dataclass
class SendToTopic(Command):
    message_dto: SendToTopicDTO = field(default_factory=SendToTopicDTO)


class SendToTopicHandler(NotificacionesCommandBaseHandler):
    def handle(self, command: SendToTopic):
        try:
            message_dto = command.message_dto
            self.message_admin.send_topic_push(
                message_dto.titulo, message_dto.cuerpo, message_dto.topico
            )
        except BusinessRuleException as bre:
            traceback.print_exc()
            raise UnprocessableEntityError(str(bre), bre.code)

        except Exception as e:
            traceback.print_exc()

            raise APIError(message=str(e), code="notificaciones.error.internal")


@execute_command.register(SendToTopic)
def command_send_to_topic(command: SendToTopic):
    SendToTopicHandler().handle(command)
