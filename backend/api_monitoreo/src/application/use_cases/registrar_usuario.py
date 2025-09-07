# src/application/use_cases/registrar_usuario.py
import bcrypt
from src.domain.entities.usuario import Usuario
from src.domain.ports.usuario_repository import IUsuarioRepository
from src.application.errors.exceptions import EmailYaRegistradoError

class RegistrarUsuario:
    """
    Caso de Uso: Registrar un nuevo usuario.
    
    Esta clase orquesta la lógica de la aplicación para el registro.
    Depende de una abstracción (el puerto IUsuarioRepository) en lugar de una
    implementación concreta, siguiendo el Principio de Inversión de Dependencias (SOLID).
    """

    def __init__(self, usuario_repository: IUsuarioRepository):
        """
        Constructor del caso de uso.
        
        Args:
            usuario_repository (IUsuarioRepository): Una implementación del repositorio
                                                     de usuarios que se inyecta como dependencia.
        """
        self.usuario_repository = usuario_repository

    def ejecutar(self, nombre, correo, clave, rol, numero_contacto=None, url_imagen_perfil=None, id_edificio_asignado=None):
        """
        Ejecuta la lógica del caso de uso.
        
        Args:
            nombre (str): Nombre del usuario.
            correo (str): Correo del usuario.
            clave (str): Contraseña en texto plano.
            rol (str): Rol del usuario.
            
        Returns:
            Usuario: La entidad del usuario recién creado.
            
        Raises:
            EmailYaRegistradoError: Si el correo ya existe en la base de datos.
        """
        # 1. Verificar si el usuario ya existe
        usuario_existente = self.usuario_repository.find_by_email(correo)
        if usuario_existente:
            raise EmailYaRegistradoError()

        # 2. Hashear la contraseña (¡NUNCA GUARDAR EN TEXTO PLANO!)
        # Usamos bcrypt para un hashing seguro.
        clave_hasheada = bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt())

        # 3. Crear la entidad de dominio Usuario
        nuevo_usuario = Usuario(
            id=None,  # El ID será generado por la base de datos
            nombre=nombre,
            correo=correo,
            clave_hash=clave_hasheada.decode('utf-8'), # Guardamos el hash como string
            rol=rol,
            numero_contacto=numero_contacto,
            url_imagen_perfil=url_imagen_perfil,
            id_edificio_asignado=id_edificio_asignado
        )

        # 4. Guardar el nuevo usuario a través del repositorio
        usuario_creado = self.usuario_repository.save(nuevo_usuario)

        return usuario_creado