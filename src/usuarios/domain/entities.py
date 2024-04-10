from dataclasses import asdict, dataclass, field

from seedwork.domain.entities import RootAggregation
from usuarios.domain.events import UsuarioCreated
from usuarios.domain.value_objects import (
    Contrasena,
    Demografia,
    Deporte,
    Identificacion,
)


@dataclass
class Usuario(RootAggregation):
    identificacion: Identificacion = field(default_factory=Identificacion)
    contrasena: Contrasena = field(init=False, repr=True)
    rol: str = field(default_factory=str)


@dataclass
class Deportista(Usuario):
    nombre: str = field(default_factory=str)
    apellido: str = field(default_factory=str)
    plan_afiliacion: str = field(default_factory=str)

    demografia: Demografia = field(default_factory=Demografia)
    deportes: list[Deporte] = field(default_factory=list)

    def create(self, correlation_id):
        self.append_event(
            UsuarioCreated(
                correlation_id=correlation_id,
                tipo_identificacion=self.identificacion.tipo,
                identificacion=self.identificacion.valor,
                rol=self.rol,
                created_at=self.created_at,
                demografia=asdict(self.demografia),
                deportes=[d.nombre for d in self.deportes],
            )
        )


@dataclass
class Organizador(Usuario):
    organizacion: str = field(default_factory=str)

    def create(self, correlation_id):
        pass


@dataclass
class Socio(Usuario):
    razon_social: str = field(default_factory=str)
    correo: str = field(default_factory=str)
    telefono: str = field(default_factory=str)

    def create(self, correlation_id):
        pass
