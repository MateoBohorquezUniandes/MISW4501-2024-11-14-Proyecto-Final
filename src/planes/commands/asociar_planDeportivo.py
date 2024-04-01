from planes.errors.errors import (
    InformacionIncompletaNoValida, PlanDeportivoNoExiste
)

# Pendiente configurar los errores
from planes.models.model import NivelExigencia, PlanDeportivo, db
from planes.commands.base_command import BaseCommannd


class AsociarPlanDeportivo(BaseCommannd):
    def __init__(
        self,
        id,
        userId
    ):
        self.id = id
        self.userId = userId

    def execute(self):

        # Definir campos mandatorios
        if not all(
            [self.id, self.userId]
        ):
            raise InformacionIncompletaNoValida
        
        planDeportivo = PlanDeportivo.query.filter_by(id=self.id).first()

        if planDeportivo is None:
            raise PlanDeportivoNoExiste

        planDeportivo.userId = str(self.userId)

        db.session.add(planDeportivo)
        db.session.commit()

        return planDeportivo
