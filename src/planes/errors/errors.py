class ApiError(Exception):
    code = 422
    description = "API Error"

class InformacionEliminada(ApiError):
    code = 200
    description = "Todos los datos fueron eliminados"

class InformacionIncompletaNoValida(ApiError):
    code = 400
    description = "Información Incompleta o no valida"