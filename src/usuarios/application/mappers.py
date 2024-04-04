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
    DeportistaDTO,
    IdentificacionDTO,
    LoginRequestDTO,
    LoginResponseDTO,
    OrganizadorDTO,
    SocioDTO,
    UsuarioDTO,
)
from usuarios.application.exceptions import BadRequestError
from usuarios.domain.entities import Deportista, Organizador, Socio, Usuario
from usuarios.domain.exceptions import InvalidRolUsuarioError
from usuarios.domain.value_objects import (
    Contrasena,
    Demografia,
    Deporte,
    Identificacion,
    LoginRequest,
    ROL,
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
            identificacion.get("tipo", ""), identificacion.get("valor", "")
        )

    def _map_to_demografia_dto(self, demografia: dict) -> DemografiaDTO:
        return DemografiaDTO(
            demografia.get("pais_nacimiento", ""),
            demografia.get("ciudad_nacimiento", ""),
            demografia.get("pais_residencia", ""),
            demografia.get("ciudad_residencia", ""),
            int(demografia.get("tiempo_residencia", 0)),
            demografia.get("genero", ""),
            int(demografia.get("edad", 0)),
            float(demografia.get("peso", 0.0)),
            float(demografia.get("altura", 0.0)),
        )

    def _map_deportista(
        self, external: dict, identificacion: IdentificacionDTO
    ) -> DeportistaDTO:
        demografia = self._map_to_demografia_dto(external.get("demografia", {}))
        deportes = external.get("deportes")

        return DeportistaDTO(
            identificacion=identificacion,
            contrasena=external.get("contrasena", ""),
            rol=ROL.DEPORTISTA.value,
            nombre=external.get("nombre", ""),
            apellido=external.get("apellido", ""),
            demografia=demografia,
            deportes=deportes,
        )

    def _map_organizador(
        self, external: dict, identificacion: IdentificacionDTO
    ) -> OrganizadorDTO:
        return OrganizadorDTO(
            identificacion=identificacion,
            contrasena=external.get("contrasena", ""),
            rol=ROL.ORGANIZADOR.value,
            organizacion=external.get("organizacion", ""),
        )

    def _map_socio(self, external: dict, identificacion: IdentificacionDTO) -> SocioDTO:
        return SocioDTO(
            identificacion=identificacion,
            contrasena=external.get("contrasena", ""),
            rol=ROL.SOCIO.value,
            razon_social=external.get("razon_social", ""),
            correo=external.get("correo", ""),
            telefono=external.get("telefono", ""),
        )

    def external_to_dto(self, external: dict) -> UsuarioDTO:
        identificacion = self._map_to_identificacion_dto(
            external.get("identificacion", {})
        )
        rol = external.get("rol", "")

        if rol == ROL.DEPORTISTA.value:
            return self._map_deportista(external, identificacion)
        elif rol == ROL.ORGANIZADOR.value:
            return self._map_organizador(external, identificacion)
        elif rol == ROL.SOCIO.value:
            return self._map_socio(external, identificacion)
        else:
            raise BadRequestError()


class LoginDTODictMapper(ApplicationMapper):
    def _map_to_identificacion_dto(self, identificacion: dict) -> IdentificacionDTO:
        return IdentificacionDTO(
            identificacion.get("tipo", ""), identificacion.get("valor", "")
        )

    def external_to_dto(self, external: any) -> LoginRequestDTO:
        identificacion = self._map_to_identificacion_dto(
            external.get("identificacion", {})
        )
        return LoginRequestDTO(
            identificacion,
            external.get("contrasena", ""),
            external.get("rol", ROL.DEPORTISTA.value),
        )

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
        return Usuario

    def _entity_to_deportista_dto(
        self, entity: Deportista, identificacion: IdentificacionDTO
    ) -> DeportistaDTO:
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
        return DeportistaDTO(
            created_at=entity.created_at.strftime(self.DATE_FORMAT),
            updated_at=entity.updated_at.strftime(self.DATE_FORMAT),
            identificacion=identificacion,
            contrasena=entity.contrasena.contrasena,
            rol=entity.rol,
            nombre=entity.nombre,
            apellido=entity.apellido,
            demografia=demografia,
            deportes=deportes,
        )

    def _entity_to_organizador_dto(
        self, entity: Organizador, identificacion: IdentificacionDTO
    ) -> DeportistaDTO:
        return OrganizadorDTO(
            created_at=entity.created_at.strftime(self.DATE_FORMAT),
            updated_at=entity.updated_at.strftime(self.DATE_FORMAT),
            identificacion=identificacion,
            contrasena=entity.contrasena.contrasena,
            rol=entity.rol,
            organizacion=entity.organizacion,
        )

    def _entity_to_socio_dto(
        self, entity: Socio, identificacion: IdentificacionDTO
    ) -> SocioDTO:
        return SocioDTO(
            created_at=entity.created_at.strftime(self.DATE_FORMAT),
            updated_at=entity.updated_at.strftime(self.DATE_FORMAT),
            identificacion=identificacion,
            contrasena=entity.contrasena.contrasena,
            rol=entity.rol,
            razon_social=entity.razon_social,
            correo=entity.correo,
            telefono=entity.telefono,
        )

    def entity_to_dto(self, entity: Usuario) -> UsuarioDTO:
        identificacion = IdentificacionDTO(
            entity.identificacion.tipo, entity.identificacion.valor
        )

        if entity.rol == ROL.DEPORTISTA.value:
            return self._entity_to_deportista_dto(entity, identificacion)
        elif entity.rol == ROL.ORGANIZADOR.value:
            return self._entity_to_organizador_dto(entity, identificacion)
        elif entity.rol == ROL.SOCIO.value:
            return self._entity_to_socio_dto(entity, identificacion)
        else:
            raise InvalidRolUsuarioError()

    def _dto_to_deportista_entity(
        self, dto: DeportistaDTO, identificacion: Identificacion
    ) -> Deportista:
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
        return Deportista(
            identificacion=identificacion,
            rol=dto.rol,
            nombre=dto.nombre,
            apellido=dto.apellido,
            demografia=demografia,
            deportes=deportes,
        )

    def _dto_to_organizador_entity(
        self, dto: OrganizadorDTO, identificacion: Identificacion
    ) -> Organizador:
        return Organizador(
            identificacion=identificacion,
            rol=dto.rol,
            organizacion=dto.organizacion,
        )

    def _dto_to_socio_entity(
        self, dto: SocioDTO, identificacion: Identificacion
    ) -> Socio:
        return Socio(
            identificacion=identificacion,
            rol=dto.rol,
            razon_social=dto.razon_social,
            correo=dto.correo,
            telefono=dto.telefono,
        )

    def dto_to_entity(self, dto: UsuarioDTO) -> Usuario:
        identificacion = Identificacion(
            dto.identificacion.tipo, dto.identificacion.valor
        )
        if dto.rol == ROL.DEPORTISTA.value:
            return self._dto_to_deportista_entity(dto, identificacion)
        elif dto.rol == ROL.ORGANIZADOR.value:
            return self._dto_to_organizador_entity(dto, identificacion)
        elif dto.rol == ROL.SOCIO.value:
            return self._dto_to_socio_entity(dto, identificacion)
        else:
            raise InvalidRolUsuarioError()


class ContrasenaMapper(UnidirectionalDomainMapper):
    def type(self) -> type:
        return Contrasena

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
        return LoginRequest

    def map(self, dto: LoginRequestDTO) -> Usuario:
        identificacion = Identificacion(
            dto.identificacion.tipo, dto.identificacion.valor
        )
        contrasena = Contrasena(contrasena=dto.contrasena)
        usuario = Usuario(identificacion=identificacion, rol=dto.rol)
        usuario.contrasena = contrasena
        return usuario
