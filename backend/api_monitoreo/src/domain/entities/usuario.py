# src/domain/entities/usuario.py

class Usuario:
    """
    Esta clase representa la entidad Usuario dentro de nuestro dominio.
    Es un objeto de Python puro que contiene los datos y la lógica de negocio
    asociada a un usuario, pero sin acoplarse a ninguna tecnología de base de datos
    o framework web. Es el corazón de nuestra regla de negocio.
    """

    def __init__(self, id, nombre, correo, clave_hash, rol, numero_contacto=None, url_imagen_perfil=None, id_edificio_asignado=None, fecha_creacion=None):
        """
        Constructor para la entidad Usuario.

        Args:
            id (int): El identificador único del usuario. Puede ser None si aún no se ha persistido.
            nombre (str): El nombre completo del usuario.
            correo (str): La dirección de correo electrónico única.
            clave_hash (str): La contraseña hasheada. ¡Nunca la contraseña en texto plano!
            rol (str): El rol del usuario (ej: 'administrador', 'conserje').
            numero_contacto (str, optional): El número de contacto. Defaults to None.
            url_imagen_perfil (str, optional): URL de la imagen de perfil. Defaults to None.
            id_edificio_asignado (int, optional): ID del edificio asignado (para conserjes). Defaults to None.
            fecha_creacion (str, optional): La fecha de creación del registro. Defaults to None.
        """
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.clave_hash = clave_hash
        self.rol = rol
        self.numero_contacto = numero_contacto
        self.url_imagen_perfil = url_imagen_perfil
        self.id_edificio_asignado = id_edificio_asignado
        self.fecha_creacion = fecha_creacion

    def to_dict(self):
        """

        Convierte la entidad Usuario en un diccionario, útil para serializar a JSON.
        Omitimos la clave_hash por seguridad.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
            "rol": self.rol,
            "numero_contacto": self.numero_contacto,
            "url_imagen_perfil": self.url_imagen_perfil,
            "id_edificio_asignado": self.id_edificio_asignado,
            "fecha_creacion": self.fecha_creacion
        }