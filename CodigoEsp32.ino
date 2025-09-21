#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <HardwareSerial.h>

// -------------------- CONFIG --------------------
const char* ssid = "nombre_wifi";
const char* password = "contraseña_wifi";
const char* serverURL = "direccion_servidor"; // e.g., "http://example.com/api/data"

// -------------------- ESTRUCTURA --------------------
struct PMS5003Data {
  uint16_t pm10_standard, pm25_standard, pm100_standard;
};

// -------------------- SENSOR MANAGER --------------------
class SensorManager {
  DHT dht;
  HardwareSerial& pmsSerial;
  PMS5003Data data;

public:
  SensorManager(uint8_t dhtPin, uint8_t dhtType, HardwareSerial& serial)
    : dht(dhtPin, dhtType), pmsSerial(serial) {}

  void begin() {
    dht.begin();
    pmsSerial.begin(9600, SERIAL_8N1, 16, 17);
    while (pmsSerial.available()) pmsSerial.read();
  }

  float readTemp() { return dht.readTemperature(); }
  float readHum() { return dht.readHumidity(); }

  PMS5003Data readPMS() {
    static PMS5003Data lastValidData = {0, 0, 0}; // para no devolver ceros si falla
    PMS5003Data emptyData = lastValidData;

    while (pmsSerial.available() >= 32) {
        // Buscar inicio de frame 0x42 0x4D
        if (pmsSerial.read() != 0x42) continue;
        if (pmsSerial.read() != 0x4D) continue;

        uint8_t frame[32];
        frame[0] = 0x42; // ya leido
        frame[1] = 0x4D;
        pmsSerial.readBytes(&frame[2], 30); // leer resto del frame

        // Calcular checksum
        uint16_t sum = 0;
        for (int i = 0; i < 30; i++) sum += frame[i];
        uint16_t checksum = (frame[30] << 8) | frame[31];

        if (sum != checksum) {
            Serial.println("Checksum inválido");
            continue; // intentar con siguiente frame
        }

        PMS5003Data data;
        data.pm10_standard  = (frame[4] << 8) | frame[5];  // PM1.0
        data.pm25_standard  = (frame[6] << 8) | frame[7];  // PM2.5
        data.pm100_standard = (frame[8] << 8) | frame[9];  // PM10

        lastValidData = data; // actualizar último valor válido
        return data;
    }

    return emptyData; // no hay frame disponible, devuelve último válido
}

};

// -------------------- DISPLAY MANAGER --------------------
class DisplayManager {
  Adafruit_SSD1306 display;

public:
  DisplayManager() : display(128, 64, &Wire, -1) {}

  bool begin() {
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
      Serial.println("Error: No se detecta la pantalla OLED");
      return false;
    }
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.println("Estacion Climática");
    display.display();
    delay(2000);
    return true;
  }

  void showReadings(float temp, float hum, PMS5003Data data) {
    display.clearDisplay();
    display.setTextSize(1);
    display.setCursor(0, 0); display.print("T: "); display.print(temp,1); display.println(" C");
    display.setCursor(0,10); display.print("H: "); display.print(hum,1); display.println(" %");
    display.setCursor(69,0); display.print("PM1.0: "); display.println(data.pm10_standard);
    display.setCursor(69,12); display.print("PM2.5: "); display.println(data.pm25_standard);
    display.setCursor(69,24); display.print("PM10: "); display.println(data.pm100_standard);
    display.display();
  }
};

// -------------------- MY NETWORK MANAGER --------------------
class MyNetworkManager {
  const char* ssid;
  const char* password;
  const char* serverURL;

public:
  MyNetworkManager(const char* s, const char* p, const char* url)
    : ssid(s), password(p), serverURL(url) {}

  void connectWiFi() {
    WiFi.begin(ssid, password);
    Serial.print("Conectando a WiFi");
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("\nConectado a WiFi");
  }

  void sendData(float temp, float hum, PMS5003Data data) {
    if (WiFi.status() != WL_CONNECTED) {
      connectWiFi();
      return;
    }

    if (isnan(temp) || isnan(hum)) {
      Serial.println("Error: Datos inválidos");
      return;
    }

    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<200> doc;
    doc["temperatura"] = temp;
    doc["humedad"] = hum;
    doc["pm1_0"] = data.pm10_standard;
    doc["pm2_5"] = data.pm25_standard;
    doc["pm10"]  = data.pm100_standard;

    String payload;
    serializeJson(doc, payload);

    int code = http.POST(payload);
    if (code <= 0) {
      Serial.println("Error enviando datos.");
    } else {
      Serial.printf("Datos enviados. Respuesta: %d\n", code);
    }
    http.end();
  }
};

// -------------------- APP CONTROLLER --------------------
class AppController {
  SensorManager sensors;
  DisplayManager display;
  MyNetworkManager network;

  unsigned long lastDisplayUpdate = 0;
  unsigned long lastSend = 0;
  const unsigned long displayInterval = 1000;   // 1 segundo
  const unsigned long sendInterval = 60000;     // 1 minuto

  float temp;
  float hum;
  PMS5003Data pms;

public:
  AppController()
    : sensors(4, DHT22, Serial2),
      network(ssid, password, serverURL) {}

  void setup() {
    Serial.begin(115200);
    network.connectWiFi();
    sensors.begin();
    if (!display.begin()) {
      while (true) delay(1000); // Error crítico
    }
    Serial.println("Iniciando estación de calidad del aire...");
  }

  void loop() {
    unsigned long now = millis();

    // Actualizar sensores
    temp = sensors.readTemp();
    hum = sensors.readHum();
    pms = sensors.readPMS();

    // Refrescar pantalla cada segundo
    if (now - lastDisplayUpdate >= displayInterval) {
      lastDisplayUpdate = now;
      display.showReadings(temp, hum, pms);

      Serial.printf("T: %.1f C | H: %.1f %% | PM1.0: %d | PM2.5: %d | PM10: %d\n",
                    temp, hum, pms.pm10_standard, pms.pm25_standard, pms.pm100_standard);
    }

    // Enviar al servidor cada minuto
    if (now - lastSend >= sendInterval) {
      lastSend = now;
      network.sendData(temp, hum, pms);
    }
  }
};

// -------------------- INSTANCIA GLOBAL --------------------
AppController app;

void setup() { app.setup(); }
void loop()  { app.loop(); }
