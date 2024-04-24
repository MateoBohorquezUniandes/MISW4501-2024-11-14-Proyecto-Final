from pydispatch import dispatcher

from sesiones.domain.events import SesionEnded

from .handlers import SesionEndedIntegrationMessageHandler

dispatcher.connect(
    SesionEndedIntegrationMessageHandler.handle,
    signal=f"{SesionEnded.__name__}Integration",
)
