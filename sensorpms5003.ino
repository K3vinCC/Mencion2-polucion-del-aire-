#include <HardwareSerial.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>

//Configuración DHT22 / AM2302 ---
#define DHTPIN 4       
#define DHTTYPE DHT22  
DHT dht(DHTPIN, DHTTYPE);

// Configuración PMS5003 ---
HardwareSerial pmsSerial(2); 

//Estructura para los datos PMS5003
struct PMS5003Data {
  uint16_t pm10_standard, pm25_standard, pm100_standard;
};

PMS5003Data data;

// Función para leer datos del PMS5003 de manera robusta
bool readPMSdata(HardwareSerial &pms) {
  while (pms.available() >= 32) {
    if (pms.peek() != 0x42) { // Cabecera de inicio
      pms.read(); // Avanza un byte para resynchronizar
      continue;
    }

    uint8_t buffer[32];
    pms.readBytes(buffer, 32);

    // Validar checksum
    uint16_t sum = 0;
    for (int i = 0; i < 30; i++) sum += buffer[i];
    uint16_t checksum = (buffer[30] << 8) | buffer[31];
    if (sum != checksum) continue; // paquete inválido, saltar

    // Guardar datos
    data.pm10_standard  = (buffer[4] << 8) | buffer[5];
    data.pm25_standard  = (buffer[6] << 8) | buffer[7];
    data.pm100_standard = (buffer[8] << 8) | buffer[9];

    return true; // paquete válido leído
  }
  return false; // no hay datos válidos
}

void setup() {
  Serial.begin(115200);
  dht.begin();

  // PMS5003 en UART2: RX=GPIO16, TX=GPIO17 (TX del PMS no es necesario)
  pmsSerial.begin(9600, SERIAL_8N1, 16, 17);

  // Limpiar buffer inicial
  while (pmsSerial.available()) pmsSerial.read();

  Serial.println("Iniciando estación de calidad del aire...");
}

void loop() {
  // --- Leer DHT22 ---
  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();

  if (!isnan(temp) && !isnan(hum)) {
    Serial.print("Temperatura: "); Serial.print(temp); Serial.print(" °C | ");
    Serial.print("Humedad: "); Serial.print(hum); Serial.println(" %");
  } else {
    Serial.println("Error leyendo DHT22");
  }

  // --- Leer PMS5003 ---
  if (readPMSdata(pmsSerial)) {
    Serial.print("PM1.0: "); Serial.print(data.pm10_standard);
    Serial.print(" µg/m³ | PM2.5: "); Serial.print(data.pm25_standard);
    Serial.print(" µg/m³ | PM10: "); Serial.println(data.pm100_standard);
  } else {
    Serial.println("Esperando datos PMS5003...");
  }

  delay(2000);
}
