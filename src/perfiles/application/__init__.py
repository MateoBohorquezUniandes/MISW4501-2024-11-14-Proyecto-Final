from pydispatch import dispatcher

from perfiles.domain.events import PerfilDemograficoModified

from .handlers import PerfilDemograficoModifiedIntegrationMessageHandler

dispatcher.connect(
    PerfilDemograficoModifiedIntegrationMessageHandler.handle,
    signal=f"{PerfilDemograficoModified.__name__}Integration",
)
