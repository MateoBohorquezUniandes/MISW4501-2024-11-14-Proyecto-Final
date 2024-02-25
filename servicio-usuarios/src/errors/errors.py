class ApiError(Exception):
    code= 422
    description = "API Error"

class InformacionIncompletaNoValida(ApiError):
    code= 400
    description= "Información Incompleta o no valida"

class CaractersEspeciales(ApiError):
    code= 400
    description= "Caracteres Especiales en nombre de usuario"

class EspacioenNombreUsuario(ApiError):
    code= 400
    description= "Espacio en nombre de usuario"

class FormatoInvalidoID(ApiError):
    code= 400
    description= "El ID no tiene un formato valido"

class UsuarioyaExiste(ApiError):
    code= 412
    description= "El Nombre de Usuario o el número de identificación ya existen en el sistema"

class UsuariooContrasenaIncorrectos(ApiError):
    code= 404
    description= "El nombre de usuario o la contrasena es incorrecto"

class InformacionIncompleta(ApiError):
    code= 400
    description= "Falta informacion en la solicitud"

class InformacionEliminada(ApiError):
    code = 200
    description = 'Todos los datos fueron eliminados'