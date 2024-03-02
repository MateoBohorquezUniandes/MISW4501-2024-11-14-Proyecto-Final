import datetime
from seedwork.application.dtos import Mapper as ApplicationMapper

from jwt_api_auth.application.dtos import TokenDTO

class CreateTokenJsonMapper(ApplicationMapper):
    def external_to_dto(self, external:any) -> TokenDTO:
        token_dto: TokenDTO = TokenDTO()
        token_dto.user = external.user
        token_dto.password = external.password
        return token_dto