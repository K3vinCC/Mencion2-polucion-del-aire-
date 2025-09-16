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