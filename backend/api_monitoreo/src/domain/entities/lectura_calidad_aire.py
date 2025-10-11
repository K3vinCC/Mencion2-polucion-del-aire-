# src/domain/entities/lectura_calidad_aire.py

class LecturaCalidadAire:
    """
    Entidad que representa una lectura de calidad del aire tomada por un dispositivo.
    """

    def __init__(self, id, id_dispositivo, pm25, pm10, co2, temperatura, humedad, timestamp=None):
        """
        Constructor para la entidad LecturaCalidadAire.

        Args:
            id (int): Identificador único de la lectura
            id_dispositivo (int): ID del dispositivo que tomó la lectura
            pm25 (float): Concentración de PM2.5 en µg/m³
            pm10 (float): Concentración de PM10 en µg/m³
            co2 (float): Concentración de CO2 en ppm
            temperatura (float): Temperatura en grados Celsius
            humedad (float): Humedad relativa en porcentaje
            timestamp (str, optional): Timestamp de la lectura
        """
        self.id = id
        self.id_dispositivo = id_dispositivo
        self.pm25 = pm25
        self.pm10 = pm10
        self.co2 = co2
        self.temperatura = temperatura
        self.humedad = humedad
        self.timestamp = timestamp

    def to_dict(self):
        """
        Convierte la entidad LecturaCalidadAire en un diccionario.
        """
        return {
            "id": self.id,
            "id_dispositivo": self.id_dispositivo,
            "pm25": self.pm25,
            "pm10": self.pm10,
            "co2": self.co2,
            "temperatura": self.temperatura,
            "humedad": self.humedad,
            "timestamp": self.timestamp
        }

    def calcular_indice_calidad(self):
        """
        Calcula un índice de calidad del aire basado en las lecturas.
        Retorna un valor entre 0-500 (similar al AQI).
        """
        # Lógica simplificada para calcular índice de calidad
        # PM2.5 tiene mayor peso que otros contaminantes
        indice_pm25 = min(self.pm25 * 2, 250)  # PM2.5 máximo contribuye 250
        indice_pm10 = min(self.pm10 * 0.5, 100)  # PM10 máximo contribuye 100
        indice_co2 = min((self.co2 - 400) * 0.1, 150)  # CO2 por encima de 400 ppm

        return round(indice_pm25 + indice_pm10 + indice_co2, 2)

    def get_categoria_calidad(self):
        """
        Retorna la categoría de calidad del aire basada en el índice.
        """
        indice = self.calcular_indice_calidad()

        if indice <= 50:
            return "Buena"
        elif indice <= 100:
            return "Moderada"
        elif indice <= 150:
            return "Dañina para grupos sensibles"
        elif indice <= 200:
            return "Dañina"
        elif indice <= 300:
            return "Muy dañina"
        else:
            return "Peligrosa"