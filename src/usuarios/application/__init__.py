from pydispatch import dispatcher

from usuarios.domain.events import UsuarioCreated

from .handlers import UsuarioCreatedIntegrationMessageHandler

dispatcher.connect(
    UsuarioCreatedIntegrationMessageHandler.handle,
    signal=f"{UsuarioCreated.__name__}Integration",
)
