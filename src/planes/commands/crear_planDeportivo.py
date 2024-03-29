from planes.errors.errors import (
    InformacionIncompletaNoValida,
)

# Pendiente configurar los errores
from planes.models.model import NivelExigencia, PlanDeportivo, db
from planes.commands.base_command import BaseCommannd


class CrearPlanDeportivo(BaseCommannd):
    def __init__(
        self,
        nombrePlan,
        nivelExigencia
    ):
        self.nombrePlan = nombrePlan
        self.nivelExigencia = nivelExigencia

    def execute(self):

        # Definir campos mandatorios
        if not all(
            [self.nombrePlan, self.nivelExigencia]
        ):
            raise InformacionIncompletaNoValida

        planDeportivo = PlanDeportivo(
            nombrePlan=self.nombrePlan,
            nivelExigencia=self.nivelExigencia
        )

        db.session.add(planDeportivo)
        db.session.commit()

        return planDeportivo
