import base64
from hashlib import sha256
from os import urandom

from seedwork.application.dtos import DTO, Mapper as ApplicationMapper
from seedwork.domain.repositories import Mapper as DomainMapper
from seedwork.domain.repositories import (
    UnidirectionalMapper as UnidirectionalDomainMapper,
)
from usuarios.application.dtos import (
    DemografiaDTO,
    IdentificacionDTO,
    LoginRequestDTO,
    LoginResponseDTO,
    UsuarioDTO,
)
from usuarios.domain.entities import Usuario
from usuarios.domain.value_objects import (
    Contrasena,
    Demografia,
    Deporte,
    Identificacion,
    LoginRequest,
)


# #####################################################################################
# Application Mappers
# #####################################################################################


class UsuarioDTODictMapper(ApplicationMapper):
    def dto_to_external(self, dto: UsuarioDTO) -> dict:
        external = dto.__dict__
        external.pop("contrasena", None)
        return external

    def _map_to_identificacion_dto(self, identificacion: dict) -> IdentificacionDTO:
        return IdentificacionDTO(
            identificacion.get("tipo"), identificacion.get("valor")
        )

    def _map_to_demografia_dto(self, demografia: dict) -> DemografiaDTO:
        return DemografiaDTO(
            demografia.get("pais_nacimiento"),
            demografia.get("ciudad_nacimiento"),
            demografia.get("pais_residencia"),
            demografia.get("ciudad_residencia"),
            int(demografia.get("tiempo_residencia")),
            demografia.get("genero"),
            int(demografia.get("edad")),
            float(demografia.get("peso")),
            float(demografia.get("altura")),
        )

    def external_to_dto(self, external: dict) -> UsuarioDTO:
        identificacion = self._map_to_identificacion_dto(external.get("identificacion"))
        demografia = self._map_to_demografia_dto(external.get("demografia"))
        deportes = external.get("deportes")

        usuario = UsuarioDTO(
            nombre=external.get("nombre"),
            apellido=external.get("apellido"),
            rol=external.get("rol"),
            contrasena=external.get("contrasena"),
            identificacion=identificacion,
            demografia=demografia,
            deportes=deportes,
        )
        return usuario


class LoginDTODictMapper(ApplicationMapper):
    def _map_to_identificacion_dto(self, identificacion: dict) -> IdentificacionDTO:
        return IdentificacionDTO(
            identificacion.get("tipo"), identificacion.get("valor")
        )

    def external_to_dto(self, external: any) -> LoginRequestDTO:
        identificacion = self._map_to_identificacion_dto(external.get("identificacion"))
        return LoginRequestDTO(identificacion, external.get("contrasena"), external.get("rol"))

    def dto_to_external(self, dto: LoginRequestDTO) -> any:
        return dto.__dict__

class AuthResponseDTODictMapper(ApplicationMapper):
    def external_to_dto(self, external: any, rol: str = "") -> LoginResponseDTO:
        return LoginResponseDTO(token=external.get("token"), rol=rol)

    def dto_to_external(self, dto: LoginResponseDTO) -> any:
        return dto.__dict__



# #####################################################################################
# Domain Mappers
# #####################################################################################


class UsuarioDTOEntityMapper(DomainMapper):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def type(self) -> type:
        return Usuario.__class__

    def entity_to_dto(self, entity: Usuario) -> UsuarioDTO:
        identificacion = IdentificacionDTO(
            entity.identificacion.tipo, entity.identificacion.valor
        )
        deportes = [d.nombre for d in entity.deportes]
        demografia = DemografiaDTO(
            entity.demografia.pais_nacimiento,
            entity.demografia.ciudad_nacimiento,
            entity.demografia.pais_residencia,
            entity.demografia.ciudad_residencia,
            entity.demografia.tiempo_residencia,
            entity.demografia.genero,
            entity.demografia.edad,
            entity.demografia.peso,
            entity.demografia.altura,
        )
        created_at = entity.created_at.strftime(self.DATE_FORMAT)
        updated_at = entity.updated_at.strftime(self.DATE_FORMAT)
        usuario = UsuarioDTO(
            created_at=created_at,
            updated_at=updated_at,
            nombre=entity.nombre,
            apellido=entity.apellido,
            rol=entity.rol,
            contrasena=entity.contrasena.contrasena,
            identificacion=identificacion,
            demografia=demografia,
            deportes=deportes,
        )
        return usuario

    def dto_to_entity(self, dto: UsuarioDTO) -> Usuario:
        identificacion = Identificacion(
            dto.identificacion.tipo, dto.identificacion.valor
        )
        deportes = [Deporte(d) for d in dto.deportes]
        demografia = Demografia(
            dto.demografia.pais_nacimiento,
            dto.demografia.ciudad_nacimiento,
            dto.demografia.pais_residencia,
            dto.demografia.ciudad_residencia,
            dto.demografia.tiempo_residencia,
            dto.demografia.genero,
            dto.demografia.edad,
            dto.demografia.peso,
            dto.demografia.altura,
        )
        usuario = Usuario(
            nombre=dto.nombre,
            apellido=dto.apellido,
            rol=dto.rol,
            identificacion=identificacion,
            demografia=demografia,
            deportes=deportes,
        )
        return usuario


class ContrasenaMapper(UnidirectionalDomainMapper):
    def type(self) -> type:
        return Contrasena.__class__

    def map(self, password: str, salt: str = None) -> Contrasena:
        salt = salt or self._generate_salt()
        return Contrasena(self._generate_password_hash(password, salt), salt)

    def _generate_salt(self) -> str:
        """
        Generates a random cryptographic 'salt' for password
        hashing and persistance

        Returns:
            str: random cryptographic 'salt'
        """
        return base64.b64encode(urandom(16)).decode("ascii")

    def _generate_password_hash(self, password: str, salt: str) -> str:
        """
        Generates password hash using original password and salt

        Args:
            password (str): _description_
            salt (str): _description_

        Returns:
            str: _description_
        """
        salted_password = f"{password}{salt}"
        return sha256(salted_password.encode()).hexdigest()


class LoginDTOEntityMapper(UnidirectionalDomainMapper):
    def type(self) -> type:
        return LoginRequest.__class__

    def map(self, dto: LoginRequestDTO) -> Usuario:
        identificacion = Identificacion(
            dto.identificacion.tipo, dto.identificacion.valor
        )
        contrasena = Contrasena(contrasena=dto.contrasena)
        usuario = Usuario(identificacion=identificacion, rol=dto.rol)
        usuario.contrasena = contrasena
        return usuario
