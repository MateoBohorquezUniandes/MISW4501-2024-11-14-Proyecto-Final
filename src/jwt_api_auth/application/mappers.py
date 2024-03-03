import datetime
from seedwork.application.dtos import Mapper as ApplicationMapper

from jwt_api_auth.application.dtos import TokenDTO

class CreateTokenJsonMapper(ApplicationMapper):
    def external_to_dto(self, external:any) -> TokenDTO:
        token_dto: TokenDTO = TokenDTO(
            external.get("user"),
            external.get("password")
            )
        return token_dto
    
    def dto_to_external(self, dto: TokenDTO) -> any:
        pass