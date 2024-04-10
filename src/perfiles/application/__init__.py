from pydispatch import dispatcher

from perfiles.domain.events import PerfilDemograficoCreated

from .handlers import PerfilDemograficoCreatedIntegrationMessageHandler

dispatcher.connect(
    PerfilDemograficoCreatedIntegrationMessageHandler.handle,
    signal=f"{PerfilDemograficoCreated.__name__}Integration",
)
