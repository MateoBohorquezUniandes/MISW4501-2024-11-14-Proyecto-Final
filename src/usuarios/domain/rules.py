from seedwork.domain.rules import BusinessRule, CompoundBusinessRule, ValidString
from usuarios.domain.entities import Usuario
from usuarios.domain.value_objects import (
    Demografia,
    Identificacion,
    TIPO_IDENTIFICACION,
    GENERO,
    ROL,
)


class _ValidTipoIdentificacion(BusinessRule):
    tipo: str

    def __init__(self, tipo, message="Tipo de identificacion invalida"):
        super().__init__(message)
        self.tipo = tipo

    def is_valid(self) -> bool:
        return self.tipo in TIPO_IDENTIFICACION.list()


class _ValidValoridentificacion(BusinessRule):
    valor: str

    def __init__(
        self, valor, message="La identificacion debe tener hasta 50 caracteres"
    ):
        super().__init__(message)
        self.valor = valor

    def is_valid(self) -> bool:
        return len(self.valor) > 0 and len(self.valor) <= 50


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

        super().__init__(message, rules)


class _ValidGenero(BusinessRule):
    genero: str

    def __init__(self, genero, message="El genero no es una opcion valida"):
        super().__init__(message)
        self.genero = genero

    def is_valid(self) -> bool:
        return self.genero in GENERO.list()


class _ValidEnteroDemografia(BusinessRule):
    valor: int
    min: int
    max: int

    def __init__(
        self, valor, min, max, message="El valor no esta dentro del rango permitido"
    ):
        super().__init__(message)
        self.valor = valor
        self.min = min
        self.max = max

    def is_valid(self) -> bool:
        return self.valor >= self.min and self.valor <= self.max


class _ValidNumeroDemografia(BusinessRule):
    valor: float
    min: float
    max: float

    def __init__(
        self, valor, min, max, message="El valor no esta dentro del rango permitido"
    ):
        super().__init__(message)
        self.valor = valor
        self.min = min
        self.max = max

    def is_valid(self) -> bool:
        return self.valor >= self.min and self.valor <= self.max


class ValidDemografia(CompoundBusinessRule):
    demografia: Demografia

    def __init__(self, demografia: Demografia, message="demografia invalida"):
        self.demografia = demografia

        rules = [
            _ValidGenero(self.demografia.genero),
            _ValidEnteroDemografia(self.demografia.tiempo_residencia, 0, 100),
            _ValidEnteroDemografia(self.demografia.edad, 18, 100),
            _ValidNumeroDemografia(self.demografia.peso, 1.0, 300.0),
            _ValidNumeroDemografia(self.demografia.altura, 1.0, 3.0),
        ]

        super().__init__(message, rules)


class _ValidRol(BusinessRule):
    rol: str

    def __init__(self, rol, message="El rol no es una opcion valida"):
        super().__init__(message)
        self.rol = rol

    def is_valid(self) -> bool:
        return self.rol in ROL.list()

class ValidUsuario(CompoundBusinessRule):
    usuario: Usuario

    def __init__(self, usuario: Usuario, message="usuario invalido"):
        self.usuario = usuario

        rules = [
            ValidString(
                self.usuario.nombre,
                1,
                250,
                "Nombre debe tener entre 10 y 250 caracteres",
            ),
            ValidString(
                self.usuario.apellido,
                1,
                250,
                "Apellido debe tener entre 10 y 250 caracteres",
            ),
            _ValidRol(self.usuario.rol),
            ValidIdentificacion(self.usuario.identificacion),
            ValidDemografia(self.usuario.demografia),
        ]

        super().__init__(message, rules)


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
            ),
        ]

        super().__init__(message, rules)

class MatchingContrasenas(CompoundBusinessRule):
    contrasena: str

    def __init__(self, contrasena: str, message="usuario invalido"):
        self.contrasena = contrasena

        rules = [
            ValidString(
                self.contrasena,
                10,
                250,
                "Contrasena debe tener entre 10 y 50 caracteres",
            ),
        ]

        super().__init__(message, rules)
