#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>   // Librería para JSON
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <HardwareSerial.h>

// -------------------- RED --------------------
const char* ssid = "nombre_wifi";
const char* password = "contraseña_wifi";
const char* serverURL = "Dominio_del_servidor"; // 

// -------------------- DHT22 --------------------
#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// -------------------- OLED --------------------
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// -------------------- PMS5003 --------------------
HardwareSerial pmsSerial(2); // UART2 del ESP32
struct PMS5003Data {
  uint16_t pm10_standard, pm25_standard, pm100_standard;
};
PMS5003Data data = {0, 0, 0};

// -------------------- FUNCIONES --------------------
void updatePMS() {
  while (pmsSerial.available() >= 32) {
    if (pmsSerial.peek() != 0x42) {
      pmsSerial.read();
      continue;
    }
    uint8_t buffer[32];
    pmsSerial.readBytes(buffer, 32);

    uint16_t sum = 0;
    for (int i = 0; i < 30; i++) sum += buffer[i];
    uint16_t checksum = (buffer[30] << 8) | buffer[31];
    if (sum != checksum) continue;

    data.pm10_standard = (buffer[4] << 8) | buffer[5];
    data.pm25_standard = (buffer[6] << 8) | buffer[7];
    data.pm100_standard = (buffer[8] << 8) | buffer[9];
    break;
  }
}

void enviarDatos(float temp, float hum, PMS5003Data pms) {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(serverURL); // HTTPS
  http.addHeader("Content-Type", "application/json");

  StaticJsonDocument<200> jsonDoc;
  jsonDoc["temperatura"] = temp;
  jsonDoc["humedad"] = hum;
  jsonDoc["pm1_0"] = pms.pm10_standard;
  jsonDoc["pm2_5"] = pms.pm25_standard;
  jsonDoc["pm10"] = pms.pm100_standard;

  String payload;
  serializeJson(jsonDoc, payload);

  int httpResponseCode = http.POST(payload);
  Serial.print("HTTP Response: "); Serial.println(httpResponseCode);

  http.end();
}

// -------------------- SETUP --------------------
void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Conectado a WiFi");

  dht.begin();

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("Error: No se detecta la pantalla OLED");
    for (;;);
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Estacion Climática");
  display.display();
  delay(2000);

  pmsSerial.begin(9600, SERIAL_8N1, 16, 17);
  while (pmsSerial.available()) pmsSerial.read();
  Serial.println("Iniciando estación de calidad del aire...");
}

// -------------------- LOOP --------------------
void loop() {
  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();
  updatePMS();

  // Mostrar Serial
  Serial.print("T: "); Serial.print(temp); Serial.print(" C | ");
  Serial.print("H: "); Serial.print(hum); Serial.print(" % | ");
  Serial.print("PM1.0: "); Serial.print(data.pm10_standard);
  Serial.print(" | PM2.5: "); Serial.print(data.pm25_standard);
  Serial.print(" | PM10: "); Serial.println(data.pm100_standard);

  // Mostrar OLED
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0); display.print("T: "); display.print(temp,1); display.println(" C");
  display.setCursor(0,10); display.print("H: "); display.print(hum,1); display.println(" %");
  display.setCursor(69,0); display.print("PM1.0: "); display.println(data.pm10_standard);
  display.setCursor(69,12); display.print("PM2.5: "); display.println(data.pm25_standard);
  display.setCursor(69,24); display.print("PM10: "); display.println(data.pm100_standard);
  display.display();

  // Enviar datos al servidor
  enviarDatos(temp, hum, data);

  delay(60000); // enviar cada 60s
}
