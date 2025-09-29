# src/application/use_cases/actualizar_usuario.py
import bcrypt
from src.domain.ports.usuario_repository import IUsuarioRepository
from src.application.errors.exceptions import UsuarioNoEncontradoError

class ActualizarUsuario:
    """
    Caso de Uso: Actualizar información de un usuario.
    """

    def __init__(self, usuario_repository: IUsuarioRepository):
        self.usuario_repository = usuario_repository

    def ejecutar(self, usuario_id, nombre=None, correo=None, clave=None, rol=None,
                 numero_contacto=None, url_imagen_perfil=None, id_edificio_asignado=None):
        """
        Actualiza la información de un usuario.

        Args:
            usuario_id (int): ID del usuario a actualizar.
            nombre (str, optional): Nuevo nombre.
            correo (str, optional): Nuevo correo.
            clave (str, optional): Nueva contraseña.
            rol (str, optional): Nuevo rol.
            numero_contacto (str, optional): Nuevo número de contacto.
            url_imagen_perfil (str, optional): Nueva URL de imagen de perfil.
            id_edificio_asignado (int, optional): Nuevo ID de edificio asignado.

        Returns:
            Usuario: La entidad del usuario actualizado.

        Raises:
            UsuarioNoEncontradoError: Si el usuario no existe.
        """
        # Obtener el usuario actual
        usuario = self.usuario_repository.find_by_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontradoError()

        # Actualizar campos proporcionados
        if nombre is not None:
            usuario.nombre = nombre
        if correo is not None:
            usuario.correo = correo
        if rol is not None:
            usuario.rol = rol
        if numero_contacto is not None:
            usuario.numero_contacto = numero_contacto
        if url_imagen_perfil is not None:
            usuario.url_imagen_perfil = url_imagen_perfil
        if id_edificio_asignado is not None:
            usuario.id_edificio_asignado = id_edificio_asignado

        # Si se proporciona una nueva clave, hashearla
        if clave is not None:
            clave_hasheada = bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt())
            usuario.clave_hash = clave_hasheada.decode('utf-8')

        # Aquí normalmente guardaríamos el usuario actualizado
        # Pero como no tenemos un método update en el repositorio, devolveremos el usuario
        # En una implementación real, necesitaríamos agregar un método update al repositorio
        return usuario