# src/application/errors/exceptions.py

class BaseError(Exception):
    """Clase base para otras excepciones personalizadas."""
    pass

class EmailYaRegistradoError(BaseError):
    """Se lanza cuando se intenta registrar un email que ya existe."""
    def __init__(self, message="El correo electrónico ya está registrado"):
        self.message = message
        super().__init__(self.message)

class CredencialesInvalidasError(BaseError):
    """Se lanza cuando las credenciales de login son incorrectas."""
    def __init__(self, message="Correo electrónico o contraseña inválidos"):
        self.message = message
        super().__init__(self.message)

class UsuarioNoEncontradoError(BaseError):
    """Se lanza cuando no se encuentra un usuario."""
    def __init__(self, message="Usuario no encontrado"):
        self.message = message
        super().__init__(self.message)

class DispositivoNoEncontradoError(BaseError):
    """Se lanza cuando no se encuentra un dispositivo."""
    def __init__(self, message="Dispositivo no encontrado"):
        self.message = message
        super().__init__(self.message)

class LecturaNoEncontradaError(BaseError):
    """Se lanza cuando no se encuentra una lectura."""
    def __init__(self, message="Lectura no encontrada"):
        self.message = message
        super().__init__(self.message)

class AsignacionNoEncontradaError(BaseError):
    """Se lanza cuando no se encuentra una asignación."""
    def __init__(self, message="Asignación no encontrada"):
        self.message = message
        super().__init__(self.message)

class TokenInvalidoError(BaseError):
    """Se lanza cuando un token JWT es inválido."""
    def __init__(self, message="Token inválido o expirado"):
        self.message = message
        super().__init__(self.message)

class PermisosInsuficientesError(BaseError):
    """Se lanza cuando un usuario no tiene permisos para una operación."""
    def __init__(self, message="Permisos insuficientes para realizar esta operación"):
        self.message = message
        super().__init__(self.message)