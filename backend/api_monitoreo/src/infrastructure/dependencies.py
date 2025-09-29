# src/infrastructure/dependencies.py
from src.adapters.persistence.sqlite_usuario_repository import SQLiteUsuarioRepository
from src.adapters.persistence.sqlite_dispositivo_repository import SQLiteDispositivoRepository
from src.adapters.persistence.sqlite_lectura_calidad_aire_repository import SQLiteLecturaCalidadAireRepository
from src.adapters.persistence.sqlite_asignacion_limpieza_repository import SQLiteAsignacionLimpiezaRepository
from src.application.use_cases.registrar_usuario import RegistrarUsuario
from src.application.use_cases.login_usuario import LoginUsuario
from src.application.use_cases.obtener_usuario import ObtenerUsuario
from src.application.use_cases.obtener_todos_usuarios import ObtenerTodosUsuarios
from src.application.use_cases.actualizar_usuario import ActualizarUsuario
from src.application.use_cases.eliminar_usuario import EliminarUsuario
from src.application.use_cases.registrar_dispositivo import RegistrarDispositivo
from src.application.use_cases.registrar_lectura import RegistrarLectura
from src.application.use_cases.crear_asignacion_limpieza import CrearAsignacionLimpieza
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
        self._dispositivo_repository = None
        self._lectura_repository = None
        self._asignacion_repository = None
        self._registrar_usuario_use_case = None
        self._login_usuario_use_case = None
        self._obtener_usuario_use_case = None
        self._obtener_todos_usuarios_use_case = None
        self._actualizar_usuario_use_case = None
        self._eliminar_usuario_use_case = None
        self._registrar_dispositivo_use_case = None
        self._registrar_lectura_use_case = None
        self._crear_asignacion_limpieza_use_case = None

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
    def dispositivo_repository(self) -> SQLiteDispositivoRepository:
        """
        Crea y devuelve una instancia del repositorio de dispositivos.
        """
        if self._dispositivo_repository is None:
            self._dispositivo_repository = SQLiteDispositivoRepository(
                db_path=current_app.config['DATABASE_PATH']
            )
        return self._dispositivo_repository

    @property
    def lectura_repository(self) -> SQLiteLecturaCalidadAireRepository:
        """
        Crea y devuelve una instancia del repositorio de lecturas.
        """
        if self._lectura_repository is None:
            self._lectura_repository = SQLiteLecturaCalidadAireRepository(
                db_path=current_app.config['DATABASE_PATH']
            )
        return self._lectura_repository

    @property
    def asignacion_repository(self) -> SQLiteAsignacionLimpiezaRepository:
        """
        Crea y devuelve una instancia del repositorio de asignaciones.
        """
        if self._asignacion_repository is None:
            self._asignacion_repository = SQLiteAsignacionLimpiezaRepository(
                db_path=current_app.config['DATABASE_PATH']
            )
        return self._asignacion_repository

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

    @property
    def obtener_usuario_use_case(self) -> ObtenerUsuario:
        """
        Caso de uso para obtener un usuario.
        """
        if self._obtener_usuario_use_case is None:
            self._obtener_usuario_use_case = ObtenerUsuario(
                usuario_repository=self.usuario_repository
            )
        return self._obtener_usuario_use_case

    @property
    def obtener_todos_usuarios_use_case(self) -> ObtenerTodosUsuarios:
        """
        Caso de uso para obtener todos los usuarios.
        """
        if self._obtener_todos_usuarios_use_case is None:
            self._obtener_todos_usuarios_use_case = ObtenerTodosUsuarios(
                usuario_repository=self.usuario_repository
            )
        return self._obtener_todos_usuarios_use_case

    @property
    def actualizar_usuario_use_case(self) -> ActualizarUsuario:
        """
        Caso de uso para actualizar un usuario.
        """
        if self._actualizar_usuario_use_case is None:
            self._actualizar_usuario_use_case = ActualizarUsuario(
                usuario_repository=self.usuario_repository
            )
        return self._actualizar_usuario_use_case

    @property
    def eliminar_usuario_use_case(self) -> EliminarUsuario:
        """
        Caso de uso para eliminar un usuario.
        """
        if self._eliminar_usuario_use_case is None:
            self._eliminar_usuario_use_case = EliminarUsuario(
                usuario_repository=self.usuario_repository
            )
        return self._eliminar_usuario_use_case

    @property
    def registrar_dispositivo_use_case(self) -> RegistrarDispositivo:
        """
        Caso de uso para registrar dispositivos.
        """
        if self._registrar_dispositivo_use_case is None:
            self._registrar_dispositivo_use_case = RegistrarDispositivo(
                dispositivo_repository=self.dispositivo_repository
            )
        return self._registrar_dispositivo_use_case

    @property
    def registrar_lectura_use_case(self) -> RegistrarLectura:
        """
        Caso de uso para registrar lecturas.
        """
        if self._registrar_lectura_use_case is None:
            self._registrar_lectura_use_case = RegistrarLectura(
                lectura_repository=self.lectura_repository,
                dispositivo_repository=self.dispositivo_repository
            )
        return self._registrar_lectura_use_case

    @property
    def crear_asignacion_limpieza_use_case(self) -> CrearAsignacionLimpieza:
        """
        Caso de uso para crear asignaciones de limpieza.
        """
        if self._crear_asignacion_limpieza_use_case is None:
            self._crear_asignacion_limpieza_use_case = CrearAsignacionLimpieza(
                asignacion_repository=self.asignacion_repository,
                usuario_repository=self.usuario_repository,
                lectura_repository=self.lectura_repository
            )
        return self._crear_asignacion_limpieza_use_case

# Creamos una instancia global del contenedor que será accesible en toda la app
container = Container()