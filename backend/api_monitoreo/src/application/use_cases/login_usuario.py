# src/application/use_cases/login_usuario.py
import bcrypt
from src.domain.ports.usuario_repository import IUsuarioRepository
from src.application.errors.exceptions import CredencialesInvalidasError

class LoginUsuario:
    """
    Caso de Uso: Iniciar sesión de un usuario.
    
    Verifica las credenciales y, si son correctas, devuelve la entidad del usuario.
    La generación del token se manejará en la capa de adaptadores web, ya que es una
    preocupación del protocolo HTTP/API, no de la lógica de negocio pura.
    """

    def __init__(self, usuario_repository: IUsuarioRepository):
        """
        Constructor del caso de uso.
        
        Args:
            usuario_repository (IUsuarioRepository): Inyección de dependencia del repositorio.
        """
        self.usuario_repository = usuario_repository

    def ejecutar(self, correo, clave):
        """
        Ejecuta la lógica de login.
        
        Args:
            correo (str): Correo del usuario que intenta iniciar sesión.
            clave (str): Contraseña en texto plano.
            
        Returns:
            Usuario: La entidad del usuario autenticado.
            
        Raises:
            CredencialesInvalidasError: Si el correo no existe o la contraseña es incorrecta.
        """
        # 1. Buscar al usuario por su correo
        usuario = self.usuario_repository.find_by_email(correo)
        if not usuario:
            raise CredencialesInvalidasError()

        # 2. Verificar la contraseña
        # bcrypt.checkpw compara la clave en texto plano con el hash guardado.
        clave_valida = bcrypt.checkpw(clave.encode('utf-8'), usuario.clave_hash.encode('utf-8'))
        
        if not clave_valida:
            raise CredencialesInvalidasError()

        # 3. Si todo es correcto, devolver la entidad del usuario
        return usuario