from autenticador.application.dtos import IdentidadDTO, TokenRequestDTO, TokenResponseDTO
from autenticador.domain.entities import Autenticacion, Token
from autenticador.domain.value_objects import Identidad
from seedwork.application.dtos import Mapper as ApplicationMapper
from seedwork.domain.repositories import Mapper as DomainMapper


class AuthDTODictMapper(ApplicationMapper):
    def external_to_dto(self, external: dict) -> TokenRequestDTO:
        identity: IdentidadDTO = IdentidadDTO(
            external.get("tipo"), external.get("valor")
        )
        return TokenRequestDTO(identity)

    def dto_to_external(self, dto: TokenRequestDTO) -> any:
        return dto.__dict__


class AutenticacionEntityDTOMapper(DomainMapper):
    def type(self) -> type:
        return Autenticacion.__class__
    
    def dto_to_entity(self, dto: TokenRequestDTO) -> Autenticacion:
        identity: Identidad = Identidad(dto.identity.tipo, dto.identity.valor)
        return Autenticacion(identity=identity)

    def entity_to_dto(self, entity: Autenticacion) -> TokenResponseDTO:
        return TokenResponseDTO(token=entity.token.valor)
