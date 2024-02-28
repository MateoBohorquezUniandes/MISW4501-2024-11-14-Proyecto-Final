from seedwork.application.dtos import DTO, Mapper as ApplicationMapper

class PerfilDemograficoJsonDtoMapper(ApplicationMapper):

    def external_to_dto(self, external: any) -> DTO:
        return super().external_to_dto(external)
    
    def dto_to_external(self, dto: DTO) -> any:
        return dto.__dict__