# src/domain/entities/dispositivo.py

class Dispositivo:
    """
    Entidad que representa un dispositivo de monitoreo de calidad del aire.
    """

    def __init__(self, id, nombre, ubicacion, token_acceso, id_edificio, estado='activo', fecha_instalacion=None, ultima_lectura=None):
        """
        Constructor para la entidad Dispositivo.

        Args:
            id (int): Identificador único del dispositivo
            nombre (str): Nombre descriptivo del dispositivo
            ubicacion (str): Ubicación física del dispositivo
            token_acceso (str): Token único para autenticación del dispositivo
            id_edificio (int): ID del edificio donde está instalado
            estado (str): Estado del dispositivo ('activo', 'inactivo', 'mantenimiento')
            fecha_instalacion (str, optional): Fecha de instalación
            ultima_lectura (str, optional): Timestamp de la última lectura
        """
        self.id = id
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.token_acceso = token_acceso
        self.id_edificio = id_edificio
        self.estado = estado
        self.fecha_instalacion = fecha_instalacion
        self.ultima_lectura = ultima_lectura

    def to_dict(self):
        """
        Convierte la entidad Dispositivo en un diccionario.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "ubicacion": self.ubicacion,
            "token_acceso": self.token_acceso,
            "id_edificio": self.id_edificio,
            "estado": self.estado,
            "fecha_instalacion": self.fecha_instalacion,
            "ultima_lectura": self.ultima_lectura
        }