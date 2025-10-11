# src/application/use_cases/obtener_usuario.py
from src.domain.ports.usuario_repository import IUsuarioRepository
from src.application.errors.exceptions import UsuarioNoEncontradoError

class ObtenerUsuario:
    """
    Caso de Uso: Obtener información de un usuario.
    """

    def __init__(self, usuario_repository: IUsuarioRepository):
        self.usuario_repository = usuario_repository

    def ejecutar(self, usuario_id):
        """
        Obtiene un usuario por su ID.

        Args:
            usuario_id (int): ID del usuario a buscar.

        Returns:
            Usuario: La entidad del usuario encontrado.

        Raises:
            UsuarioNoEncontradoError: Si el usuario no existe.
        """
        usuario = self.usuario_repository.find_by_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontradoError()
        return usuario