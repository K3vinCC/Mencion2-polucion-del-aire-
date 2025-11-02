from abc import ABC, abstractmethod
import psycopg2

# -----------------------------
# Interfaz base para repositorios de lectura
# -----------------------------
class RepositorioLecturas(ABC):
    @abstractmethod
    def insertar(self, data: dict) -> int:
        pass

# -----------------------------
# Conexión a la base de datos
# -----------------------------
class ConexionPostgreSQL:
    DB_NAME = "nombre_base_datos"
    DB_USER = "usuario"
    DB_PASSWORD = "passwd"
    DB_HOST = "direccion"
    DB_PORT = "puerto"

    def obtener_conexion(self):
        return psycopg2.connect(
            host=self.DB_HOST,
            database=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            port=self.DB_PORT
        )

# -----------------------------
# Clase base para repositorios con validaciones
# -----------------------------
class RepositorioValidable(RepositorioLecturas):
    def __init__(self, conexion: ConexionPostgreSQL):
        self.conexion = conexion

    @property
    @abstractmethod
    def campos_obligatorios(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def reglas_validacion(self) -> dict[str, callable]:
        """Devuelve un diccionario {campo: funcion_validacion}"""
        pass

    @abstractmethod
    def query_insert(self) -> str:
        pass

    @abstractmethod
    def obtener_parametros(self, data: dict) -> tuple:
        pass

    def validar_datos(self, data: dict):
        # Validar campos obligatorios
        for campo in self.campos_obligatorios:
            if campo not in data or data[campo] is None:
                raise ValueError(f"El campo '{campo}' es obligatorio y no puede ser None")
        # Validaciones especÃ­ficas
        for campo, regla in self.reglas_validacion.items():
            if campo in data and not regla(data[campo]):
                raise ValueError(f"Valor invalido para '{campo}': {data[campo]}")

    def insertar(self, data: dict) -> int:
        self.validar_datos(data)
        conn = self.conexion.obtener_conexion()
        try:
            with conn.cursor() as cur:
                cur.execute(self.query_insert(), self.obtener_parametros(data))
                id_insertado = cur.fetchone()[0]
                conn.commit()
                return id_insertado
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

# -----------------------------
# Repositorios concretos
# -----------------------------
class LecturaTemperaturaRepositorio(RepositorioValidable):
    campos_obligatorios = ["dispositivo_id", "grados_temperatura"]
    reglas_validacion = {
        "grados_temperatura": lambda x: -50 <= x <= 60
    }

    def query_insert(self) -> str:
        return """
            INSERT INTO lecturas_temperatura (dispositivo_id, grados_temperatura, etiqueta)
            VALUES (%s, %s, %s) RETURNING id;
        """

    def obtener_parametros(self, data: dict) -> tuple:
        return (data["dispositivo_id"], data["grados_temperatura"], data.get("etiqueta"))

class LecturaHumedadRepositorio(RepositorioValidable):
    campos_obligatorios = ["dispositivo_id", "porcentaje_humedad"]
    reglas_validacion = {
        "porcentaje_humedad": lambda x: 0 <= x <= 100
    }

    def query_insert(self) -> str:
        return """
            INSERT INTO lecturas_humedad (dispositivo_id, porcentaje_humedad, etiqueta)
            VALUES (%s, %s, %s) RETURNING id;
        """

    def obtener_parametros(self, data: dict) -> tuple:
        return (data["dispositivo_id"], data["porcentaje_humedad"], data.get("etiqueta"))

class LecturaCalidadAireRepositorio(RepositorioValidable):
    campos_obligatorios = ["dispositivo_id", "valor_pm1", "valor_pm2_5", "valor_pm10"]
    reglas_validacion = {
        "valor_pm1": lambda x: x >= 0,
        "valor_pm2_5": lambda x: x >= 0,
        "valor_pm10": lambda x: x >= 0
    }

    def query_insert(self) -> str:
        return """
            INSERT INTO lecturas_calidad_aire (dispositivo_id, valor_pm1, valor_pm2_5, valor_pm10, etiqueta)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """

    def obtener_parametros(self, data: dict) -> tuple:
        return (
            data["dispositivo_id"],
            data["valor_pm1"],
            data["valor_pm2_5"],
            data["valor_pm10"],
            data.get("etiqueta")
        )

# -----------------------------
# Simulación de envío de datos
# -----------------------------
if __name__ == "__main__":
    conexion = ConexionPostgreSQL()

    temp_repo = LecturaTemperaturaRepositorio(conexion)
    humedad_repo = LecturaHumedadRepositorio(conexion)
    aire_repo = LecturaCalidadAireRepositorio(conexion)