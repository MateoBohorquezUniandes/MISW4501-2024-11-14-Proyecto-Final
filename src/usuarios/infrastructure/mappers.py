from seedwork.domain.repositories import Mapper
from usuarios.domain.entities import Deportista, Organizador, Socio, Usuario
from usuarios.domain.value_objects import (
    Contrasena,
    Demografia,
    Deporte,
    Identificacion,
)
from usuarios.infrastructure.dtos import Deportista as DeportistaDTO
from usuarios.infrastructure.dtos import Organizador as OrganizadorDTO
from usuarios.infrastructure.dtos import Socio as SocioDTO


class DeportistaMapper(Mapper):
    def type(self) -> type:
        return Usuario

    def entity_to_dto(self, entity: Deportista) -> DeportistaDTO:
        deportista_dto = DeportistaDTO()
        deportista_dto.tipo_identificacion = entity.identificacion.tipo
        deportista_dto.identificacion = entity.identificacion.valor
        deportista_dto.rol = entity.rol
        deportista_dto.contrasena = entity.contrasena.contrasena
        deportista_dto.salt = entity.contrasena.salt

        deportista_dto.nombre = entity.nombre
        deportista_dto.apellido = entity.apellido
        deportista_dto.plan_afiliacion = entity.plan_afiliacion
        deportista_dto.genero = entity.demografia.genero
        deportista_dto.edad = entity.demografia.edad
        deportista_dto.peso = entity.demografia.peso
        deportista_dto.altura = entity.demografia.altura
        deportista_dto.pais_nacimiento = entity.demografia.pais_nacimiento
        deportista_dto.ciudad_nacimiento = entity.demografia.ciudad_nacimiento
        deportista_dto.pais_residencia = entity.demografia.pais_residencia
        deportista_dto.ciudad_residencia = entity.demografia.ciudad_residencia
        deportista_dto.tiempo_residencia = entity.demografia.tiempo_residencia
        deportista_dto.deportes = "".join([d.nombre for d in entity.deportes])

        return deportista_dto

    def dto_to_entity(self, dto: DeportistaDTO) -> Deportista:
        identificacion = Identificacion(dto.tipo_identificacion, dto.identificacion)
        contrasena = Contrasena(dto.contrasena, dto.salt)
        demografia = Demografia(
            dto.pais_nacimiento,
            dto.ciudad_nacimiento,
            dto.pais_residencia,
            dto.ciudad_residencia,
            dto.tiempo_residencia,
            dto.genero,
            dto.edad,
            dto.peso,
            dto.altura,
        )
        deportes = [Deporte(d) for d in dto.deportes.split(",")]

        deportista = Deportista(
            identificacion=identificacion,
            rol=dto.rol,
            plan_afiliacion=dto.plan_afiliacion,
            nombre=dto.nombre,
            apellido=dto.apellido,
            demografia=demografia,
            deportes=deportes,
        )
        deportista.contrasena = contrasena
        return deportista


class OrganizadorMapper(Mapper):
    def type(self) -> type:
        return Usuario

    def entity_to_dto(self, entity: Organizador) -> OrganizadorDTO:
        organizador_dto = OrganizadorDTO()
        organizador_dto.tipo_identificacion = entity.identificacion.tipo
        organizador_dto.identificacion = entity.identificacion.valor
        organizador_dto.rol = entity.rol
        organizador_dto.contrasena = entity.contrasena.contrasena
        organizador_dto.salt = entity.contrasena.salt

        organizador_dto.organizacion = entity.organizacion
        return organizador_dto

    def dto_to_entity(self, dto: OrganizadorDTO) -> Organizador:
        identificacion = Identificacion(dto.tipo_identificacion, dto.identificacion)
        contrasena = Contrasena(dto.contrasena, dto.salt)

        organizador = Organizador(
            identificacion=identificacion, rol=dto.rol, organizacion=dto.organizacion
        )
        organizador.contrasena = contrasena
        return organizador


class SocioMapper(Mapper):
    def type(self) -> type:
        return Usuario

    def entity_to_dto(self, entity: Socio) -> SocioDTO:
        socio_dto = SocioDTO()
        socio_dto.tipo_identificacion = entity.identificacion.tipo
        socio_dto.identificacion = entity.identificacion.valor
        socio_dto.rol = entity.rol
        socio_dto.contrasena = entity.contrasena.contrasena
        socio_dto.salt = entity.contrasena.salt

        socio_dto.razon_social = entity.razon_social
        socio_dto.correo = entity.correo
        socio_dto.telefono = entity.telefono
        return socio_dto

    def dto_to_entity(self, dto: SocioDTO) -> Socio:
        identificacion = Identificacion(dto.tipo_identificacion, dto.identificacion)
        contrasena = Contrasena(dto.contrasena, dto.salt)

        socio = Socio(
            identificacion=identificacion,
            rol=dto.rol,
            razon_social=dto.razon_social,
            correo=dto.correo,
            telefono=dto.telefono,
        )
        socio.contrasena = contrasena
        return socio
