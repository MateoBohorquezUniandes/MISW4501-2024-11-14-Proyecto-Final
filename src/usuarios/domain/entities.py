
from dataclasses import dataclass, field

from seedwork.domain.entities import RootAggregation
from usuarios.domain.events import UsuarioCreated
from usuarios.domain.value_objects import Contrasena, Demografia, Deporte, Identificacion


@dataclass
class Usuario(RootAggregation):
    nombre: str = field(default_factory=str)
    apellido: str = field(default_factory=str)

    rol: str = field(default_factory=str)
    contrasena: Contrasena = field(init=False, repr=True)
    identificacion: Identificacion = field(default_factory=Identificacion)

    demografia: Demografia = field(default_factory=Demografia)
    deportes: list[Deporte] = field(default_factory=list)

    def create(self, correlation_id):
        self.append_event(
            UsuarioCreated(
                correlation_id=correlation_id,
                id_usuario=self.id,
                created_at=self.created_at,
                demografia=self.demografia.__dict__,
                deportes=[d.nombre for d in self.deportes]
            )
        )
