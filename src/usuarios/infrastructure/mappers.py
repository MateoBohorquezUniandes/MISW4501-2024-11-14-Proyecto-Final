from seedwork.domain.repositories import Mapper, UnidirectionalMapper
from usuarios.domain.entities import Usuario
from usuarios.domain.value_objects import (
    Contrasena,
    Demografia,
    Deporte,
    Identificacion,
)
from usuarios.infrastructure.dtos import Usuario as UsuarioDTO


class UsuarioMapper(Mapper):
    def type(self) -> type:
        return Usuario.__class__

    def entity_to_dto(self, entity: Usuario) -> UsuarioDTO:
        usuario_dto = UsuarioDTO()
        usuario_dto.tipo_identificacion = entity.identificacion.tipo
        usuario_dto.identificacion = entity.identificacion.valor
        usuario_dto.rol = entity.rol
        usuario_dto.contrasena = entity.contrasena.contrasena
        usuario_dto.salt = entity.contrasena.salt
        usuario_dto.nombre = entity.nombre
        usuario_dto.apellido = entity.apellido
        usuario_dto.genero = entity.demografia.genero
        usuario_dto.edad = entity.demografia.edad
        usuario_dto.peso = entity.demografia.peso
        usuario_dto.altura = entity.demografia.altura
        usuario_dto.pais_nacimiento = entity.demografia.pais_nacimiento
        usuario_dto.ciudad_nacimiento = entity.demografia.ciudad_nacimiento
        usuario_dto.pais_residencia = entity.demografia.pais_residencia
        usuario_dto.ciudad_residencia = entity.demografia.ciudad_residencia
        usuario_dto.tiempo_residencia = entity.demografia.tiempo_residencia
        usuario_dto.deportes = "".join([d.nombre for d in entity.deportes])

        return usuario_dto

    def dto_to_entity(self, dto: UsuarioDTO) -> Usuario:
        identificacion = Identificacion(dto.tipo_identificacion, dto.identificacion)
        deportes = [Deporte(d) for d in dto.deportes.split(",")]
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
        usuario = Usuario(
            nombre=dto.nombre,
            apellido=dto.apellido,
            rol=dto.rol,
            identificacion=identificacion,
            demografia=demografia,
            deportes=deportes,
        )
        contrasena = Contrasena(dto.contrasena, dto.salt)
        usuario.contrasena = contrasena
        return usuario
