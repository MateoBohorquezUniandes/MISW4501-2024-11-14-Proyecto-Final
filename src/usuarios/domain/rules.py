from re import fullmatch

from seedwork.domain.rules import (
    BusinessRule,
    CompoundBusinessRule,
    ValidFloat,
    ValidInteger,
    ValidString,
)
from seedwork.domain.value_objects import GENERO
from usuarios.domain.entities import Deportista, Organizador, Socio
from usuarios.domain.value_objects import (
    ROL,
    TIPO_IDENTIFICACION,
    Demografia,
    Identificacion,
    TIPO_IDENTIFICACION,
    GENERO,
    ROL,
    PLAN_AFILIACION
)


class _ValidTipoIdentificacion(BusinessRule):
    tipo: str

    def __init__(self, tipo, message="Tipo de identificacion invalida"):
        super().__init__(message, "tipo")
        self.tipo = tipo

    def is_valid(self) -> bool:
        return self.tipo in TIPO_IDENTIFICACION.list()


class _ValidValoridentificacion(BusinessRule):
    valor: str

    def __init__(
        self, valor, message="La identificacion debe tener hasta 50 caracteres"
    ):
        super().__init__(message, "valor")
        self.valor = valor

    def is_valid(self) -> bool:
        return len(self.valor) > 0 and len(self.valor) <= 20


class ValidIdentificacion(CompoundBusinessRule):
    identificacion: Identificacion

    def __init__(
        self, identificacion: Identificacion, message="identificacion invalida"
    ):
        self.identificacion = identificacion

        rules = [
            _ValidTipoIdentificacion(self.identificacion.tipo),
            _ValidValoridentificacion(self.identificacion.valor),
        ]

        super().__init__(message, rules, "validation.identificacion")


class _ValidGenero(BusinessRule):
    genero: str

    def __init__(self, genero, message="El genero no es una opcion valida"):
        super().__init__(message, "genero")
        self.genero = genero

    def is_valid(self) -> bool:
        return self.genero in GENERO.list()


class ValidDemografia(CompoundBusinessRule):
    demografia: Demografia

    def __init__(self, demografia: Demografia, message="demografia invalida"):
        self.demografia = demografia

        rules = [
            _ValidGenero(self.demografia.genero),
            ValidInteger(
                self.demografia.tiempo_residencia,
                0,
                100,
                "tiempo residencia fuera del rango",
                "residencia.tiempo",
            ),
            ValidInteger(self.demografia.edad, 18, 100, "edad fuera del rango", "edad"),
            ValidFloat(
                self.demografia.peso, 1.0, 300.0, "peso fuera del rango", "peso"
            ),
            ValidFloat(
                self.demografia.altura, 1.0, 3.0, "altura fuera del rango", "altura"
            ),
        ]

        super().__init__(message, rules, "demografia")


class ValidRol(BusinessRule):
    rol: str

    def __init__(self, rol, message="El rol no es una opcion valida"):
        super().__init__(message, "validation.rol")
        self.rol = rol

    def is_valid(self) -> bool:
        return self.rol in ROL.list()

#Regla Plan Afiliacion
class ValidPlanAfiliacion(BusinessRule):
    planAfiliacion: str

    def __init__(self, planAfiliacion, message="El plan de afiliacion no es una opcion valida"):
        super().__init__(message, "validation.planAfiliacion")
        self.planAfiliacion = planAfiliacion

    def is_valid(self) -> bool:
        return self.planAfiliacion in PLAN_AFILIACION.list()


class ValidEmail(BusinessRule):
    email: str
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

    def __init__(self, email, message="email invalido"):
        super().__init__(message, "validation.email")
        self.email = email

    def is_valid(self) -> bool:
        return fullmatch(self.regex, self.email)


class ValidDeportista(CompoundBusinessRule):
    usuario: Deportista

    def __init__(self, usuario: Deportista, message="deportista invalido"):
        self.usuario = usuario

        rules = [
            ValidString(
                self.usuario.nombre,
                1,
                250,
                "Nombre debe tener entre 10 y 250 caracteres",
                "nombre",
            ),
            ValidString(
                self.usuario.apellido,
                1,
                250,
                "Apellido debe tener entre 10 y 250 caracteres",
                "apellido",
            ),
            ValidRol(self.usuario.rol),
            ValidIdentificacion(self.usuario.identificacion),
            ValidDemografia(self.usuario.demografia),
        ]

        super().__init__(message, rules, "validation.usuario")


class ValidOrganizador(CompoundBusinessRule):
    usuario: Organizador

    def __init__(self, usuario: Organizador, message="organizador invalido"):
        self.usuario = usuario

        rules = [
            ValidIdentificacion(self.usuario.identificacion),
            ValidRol(self.usuario.rol),
            ValidString(
                self.usuario.organizacion,
                1,
                250,
                "Nombre de la organizacion debe tener entre 10 y 250 caracteres",
                "organizacion",
            ),
        ]

        super().__init__(message, rules, "validation.usuario")


class ValidSocio(CompoundBusinessRule):
    usuario: Socio

    def __init__(self, usuario: Socio, message="socio invalido"):
        self.usuario = usuario

        rules = [
            ValidIdentificacion(self.usuario.identificacion),
            ValidRol(self.usuario.rol),
            ValidString(
                self.usuario.razon_social,
                1,
                250,
                "Razon Social debe tener entre 10 y 250 caracteres",
                "razon_social",
            ),
            ValidEmail(self.usuario.correo),
            ValidString(
                self.usuario.telefono,
                1,
                250,
                "Telefono debe tener entre 10 y 250 caracteres",
                "telefono",
            ),
        ]

        super().__init__(message, rules, "validation.usuario")


class ValidContrasena(CompoundBusinessRule):
    contrasena: str

    def __init__(self, contrasena: str, message="usuario invalido"):
        self.contrasena = contrasena

        rules = [
            ValidString(
                self.contrasena,
                10,
                250,
                "Contrasena debe tener entre 10 y 50 caracteres",
                "credenciales",
            ),
        ]

        super().__init__(message, rules, "validation.login")
