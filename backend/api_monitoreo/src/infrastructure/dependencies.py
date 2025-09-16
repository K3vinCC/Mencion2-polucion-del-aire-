# src/infrastructure/dependencies.py
from src.adapters.persistence.sqlite_usuario_repository import SQLiteUsuarioRepository
from src.application.use_cases.registrar_usuario import RegistrarUsuario
from src.application.use_cases.login_usuario import LoginUsuario
from flask import current_app

class Container:
    """
    Contenedor para la Inyección de Dependencias.
    
    Centraliza la creación de instancias de nuestras clases (adaptadores, casos de uso),
    asegurando que cada componente reciba las dependencias que necesita para funcionar.
    """

    def __init__(self):
        # El contenedor se inicializa vacío y se configura después
        self._usuario_repository = None
        self._registrar_usuario_use_case = None
        self._login_usuario_use_case = None

    @property
    def usuario_repository(self) -> SQLiteUsuarioRepository:
        """
        Crea y devuelve una instancia única (Singleton) del repositorio de usuarios.
        Utiliza la ruta de la base de datos configurada en la app de Flask.
        """
        if self._usuario_repository is None:
            self._usuario_repository = SQLiteUsuarioRepository(
                db_path=current_app.config['DATABASE_PATH']
            )
        return self._usuario_repository

    @property
    def registrar_usuario_use_case(self) -> RegistrarUsuario:
        """
        Crea y devuelve una instancia del caso de uso para registrar usuarios,
        inyectándole el repositorio de usuarios.
        """
        if self._registrar_usuario_use_case is None:
            self._registrar_usuario_use_case = RegistrarUsuario(
                usuario_repository=self.usuario_repository
            )
        return self._registrar_usuario_use_case

    @property
    def login_usuario_use_case(self) -> LoginUsuario:
        """
        Crea y devuelve una instancia del caso de uso para el login,
        inyectándole el repositorio de usuarios.
        """
        if self._login_usuario_use_case is None:
            self._login_usuario_use_case = LoginUsuario(
                usuario_repository=self.usuario_repository
            )
        return self._login_usuario_use_case

# Creamos una instancia global del contenedor que será accesible en toda la app
container = Container()