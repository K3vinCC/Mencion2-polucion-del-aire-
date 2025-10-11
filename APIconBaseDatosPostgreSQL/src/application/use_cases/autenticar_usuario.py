# src/application/use_cases/autenticar_usuario.py
"""
Caso de uso: Autenticar Usuario
Permite a un usuario iniciar sesión en el sistema mediante email y contraseña.
"""

import bcrypt
from src.domain.ports.usuario_repository import IUsuarioRepository
from src.domain.entities.usuario import Usuario


class AutenticarUsuario:
    """
    Caso de uso para autenticar usuarios en el sistema.

    Verifica las credenciales proporcionadas y retorna el usuario
    si la autenticación es exitosa.
    """

    def __init__(self, usuario_repository: IUsuarioRepository):
        """
        Constructor del caso de uso.

        Args:
            usuario_repository: Repositorio de usuarios inyectado
        """
        self.usuario_repository = usuario_repository

    def ejecutar(self, email: str, password: str) -> Usuario:
        """
        Ejecuta la autenticación del usuario.

        Args:
            email: Email del usuario que intenta autenticarse
            password: Contraseña en texto plano

        Returns:
            Usuario: La entidad del usuario autenticado

        Raises:
            ValueError: Si las credenciales son inválidas o el usuario no existe
        """
        # Validar entrada
        if not email or not password:
            raise ValueError("Email y contraseña son requeridos")

        # Buscar usuario por email
        usuario = self.usuario_repository.find_by_email(email)
        if not usuario:
            raise ValueError("Credenciales inválidas")

        # Verificar contraseña
        if not self._verificar_password(password, usuario.clave_hash):
            raise ValueError("Credenciales inválidas")

        return usuario

    def _verificar_password(self, password: str, hash_almacenado: str) -> bool:
        """
        Verifica si la contraseña proporcionada coincide con el hash almacenado.

        Args:
            password: Contraseña en texto plano
            hash_almacenado: Hash bcrypt almacenado en la base de datos

        Returns:
            bool: True si la contraseña es correcta
        """
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                hash_almacenado.encode('utf-8')
            )
        except Exception:
            return False