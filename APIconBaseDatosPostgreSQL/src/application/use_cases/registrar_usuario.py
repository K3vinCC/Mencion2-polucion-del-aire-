# src/application/use_cases/registrar_usuario.py
"""
Caso de uso: Registrar Usuario
Permite crear nuevos usuarios en el sistema con validaciones de negocio.
"""

import bcrypt
from src.domain.ports.usuario_repository import IUsuarioRepository
from src.domain.entities.usuario import Usuario


class RegistrarUsuario:
    """
    Caso de uso para registrar nuevos usuarios en el sistema.

    Maneja la creación de usuarios con validaciones de negocio,
    encriptación de contraseñas y asignación de roles.
    """

    def __init__(self, usuario_repository: IUsuarioRepository):
        """
        Constructor del caso de uso.

        Args:
            usuario_repository: Repositorio de usuarios inyectado
        """
        self.usuario_repository = usuario_repository

    def ejecutar(
        self,
        email: str,
        password: str,
        nombre_completo: str,
        rol_id: int,
        universidad_id: int = None
    ) -> Usuario:
        """
        Ejecuta el registro de un nuevo usuario.

        Args:
            email: Email único del usuario
            password: Contraseña en texto plano (mínimo 8 caracteres)
            nombre_completo: Nombre completo del usuario
            rol_id: ID del rol (1=SuperAdmin, 2=Admin_Universidad, 3=Conserje, 4=Limpiador)
            universidad_id: ID de la universidad (requerido para roles no SuperAdmin)

        Returns:
            Usuario: La entidad del usuario recién creado

        Raises:
            ValueError: Si los datos son inválidos o ya existe un usuario con ese email
        """
        # Validaciones de entrada
        self._validar_datos(email, password, nombre_completo, rol_id, universidad_id)

        # Verificar que no exista un usuario con el mismo email
        usuario_existente = self.usuario_repository.find_by_email(email)
        if usuario_existente:
            raise ValueError("Ya existe un usuario con este email")

        # Generar hash de la contraseña
        password_hash = self._generar_password_hash(password)

        # Crear entidad de usuario
        nuevo_usuario = Usuario(
            id=None,
            email=email,
            clave_hash=password_hash,
            nombre_completo=nombre_completo,
            rol_id=rol_id,
            universidad_id=universidad_id
        )

        # Guardar en el repositorio
        usuario_creado = self.usuario_repository.save(nuevo_usuario)

        return usuario_creado

    def _validar_datos(
        self,
        email: str,
        password: str,
        nombre_completo: str,
        rol_id: int,
        universidad_id: int = None
    ):
        """
        Valida los datos de entrada según reglas de negocio.

        Args:
            email: Email a validar
            password: Contraseña a validar
            nombre_completo: Nombre a validar
            rol_id: Rol a validar
            universidad_id: Universidad a validar

        Raises:
            ValueError: Si algún dato es inválido
        """
        # Validar email
        if not email or '@' not in email:
            raise ValueError("Email inválido")

        # Validar contraseña
        if not password or len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")

        # Validar nombre
        if not nombre_completo or len(nombre_completo.strip()) < 2:
            raise ValueError("El nombre completo es requerido y debe tener al menos 2 caracteres")

        # Validar rol
        roles_validos = [1, 2, 3, 4]  # SuperAdmin, Admin_Universidad, Conserje, Limpiador
        if rol_id not in roles_validos:
            raise ValueError("Rol inválido")

        # Validar universidad_id para roles que no son SuperAdmin
        if rol_id != 1 and universidad_id is None:
            raise ValueError("La universidad es requerida para este rol")

        # Los SuperAdmin no deben tener universidad asignada
        if rol_id == 1 and universidad_id is not None:
            raise ValueError("Los SuperAdmin no deben tener universidad asignada")

    def _generar_password_hash(self, password: str) -> str:
        """
        Genera un hash seguro para la contraseña usando bcrypt.

        Args:
            password: Contraseña en texto plano

        Returns:
            str: Hash de la contraseña
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')