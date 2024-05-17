from notificaciones.infrastructure.firebase_messaging import MessageAdmin
from seedwork.application.commands import CommandHandler


class NotificacionesCommandBaseHandler(CommandHandler):
    def __init__(self):
        self._message_admin: MessageAdmin = MessageAdmin()

    @property
    def message_admin(self):
        return self._message_admin
