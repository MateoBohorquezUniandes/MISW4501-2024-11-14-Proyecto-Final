from dataclasses import dataclass, field
from uuid import UUID

from seedwork.domain.value_objects import ExtendedEnum, ValueObject
from usuarios.domain.exceptions import InvalidPasswordMatchError


class ROL(ExtendedEnum):
    DEPORTISTA = "DEPORTISTA"
    ORGANIZADOR = "ORGANIZADOR"
    SOCIO = "SOCIO"


class TIPO_IDENTIFICACION(ExtendedEnum):
    DOCUMENTO_IDENTIDAD = "DNI"
    CEDULA_CIUDADANIA = "CC"
    CEDULA_EXTRANGERIA = "CE"


class GENERO(ExtendedEnum):
    MASCULINO = "M"
    FEMENINO = "F"
    OTRO = "O"


@dataclass(frozen=True)
class Identificacion(ValueObject):
    tipo: str = field(default_factory=str)
    valor: str = field(default_factory=str)


@dataclass(frozen=True)
class Demografia(ValueObject):
    pais_nacimiento: str = field(default_factory=str)
    ciudad_nacimiento: str = field(default_factory=str)
    pais_residencia: str = field(default_factory=str)
    ciudad_residencia: str = field(default_factory=str)
    tiempo_residencia: int = field(default_factory=int)

    genero: str = field(default_factory=str)
    edad: int = field(default_factory=int)
    peso: float = field(default_factory=float)
    altura: float = field(default_factory=float)


@dataclass(frozen=True)
class Deporte(ValueObject):
    nombre: str = field(default_factory=str)


@dataclass(frozen=True)
class Contrasena(ValueObject):
    contrasena: str = field(default_factory=str)
    salt: UUID = field(default_factory=str, repr=True)

    def match(self, password, raise_exception=False):
        check = self.contrasena == password
        if not check and raise_exception:
            raise InvalidPasswordMatchError()
        return check


class LoginRequest(ValueObject):
    identificacion: Identificacion = field(default_factory=Identificacion)
    contrasena: Contrasena = field(default_factory=Contrasena)
    rol: str = field(default_factory=str)
