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
const char* ssid = "usuario";
const char* password = "passwd";

const char* loginURL = "direccion_ip/login";
const char* serverURL = "direccion_ip/datos";

// Credenciales del dispositivo
const char* device_id = "id_esp32";
const char* device_secret = "credenciassha_256";

String jwtToken = "";

// -------------------- ESTRUCTURA --------------------
struct PMS5003Data {
  uint16_t pm10_standard, pm25_standard, pm100_standard;
};

// -------------------- SENSOR MANAGER --------------------
class SensorManager {
  DHT dht;
  HardwareSerial& pmsSerial;

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
    PMS5003Data pmsData = {0, 0, 0};
    if (pmsSerial.available() >= 32) {
      if (pmsSerial.read() == 0x42 && pmsSerial.read() == 0x4D) {
        uint8_t frame[32];
        frame[0] = 0x42;
        frame[1] = 0x4D;
        pmsSerial.readBytes(&frame[2], 30);

        uint16_t pm1 = (frame[4] << 8) | frame[5];
        uint16_t pm25 = (frame[6] << 8) | frame[7];
        uint16_t pm10 = (frame[8] << 8) | frame[9];

        pmsData = {pm1, pm25, pm10};
      }
    }
    return pmsData;
  }
};

// -------------------- DISPLAY MANAGER --------------------
class DisplayManager {
  Adafruit_SSD1306 display;

public:
  DisplayManager() : display(128, 64, &Wire, -1) {}

  bool begin() {
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
      Serial.println("Error: OLED no detectada");
      return false;
    }
    display.clearDisplay();
    display.display();
    return true;
  }

  void showReadings(float temp, float hum, PMS5003Data data) {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0); display.printf("T: %.1f C\n", temp);
    display.setCursor(0,12); display.printf("H: %.1f %%\n", hum);
    display.setCursor(0,24); display.printf("PM1: %d\n", data.pm10_standard);
    display.setCursor(0,36); display.printf("PM2.5: %d\n", data.pm25_standard);
    display.setCursor(0,48); display.printf("PM10: %d\n", data.pm100_standard);
    display.display();
  }
};

// -------------------- NETWORK MANAGER --------------------
class MyNetworkManager {
public:
  void connectWiFi() {
    WiFi.begin(ssid, password);
    Serial.print("Conectando WiFi");
    while (WiFi.status() != WL_CONNECTED) {
      Serial.print(".");
      delay(500);
    }
    Serial.println("\n✅ WiFi Conectado");
  }

  bool loginDevice() {
    if (WiFi.status() != WL_CONNECTED) return false;

    HTTPClient http;
    http.begin(loginURL);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<200> doc;
    doc["device_id"] = device_id;
    doc["device_secret"] = device_secret;

    String body;
    serializeJson(doc, body);

    int code = http.POST(body);
    if (code == 200) {
      String response = http.getString();
      StaticJsonDocument<300> resDoc;
      deserializeJson(resDoc, response);
      jwtToken = resDoc["token"].as<String>();

      Serial.println("✅ Token actualizado!");
      http.end();
      return true;
    }

    Serial.printf("❌ Error login: %d\n", code);
    http.end();
    return false;
  }

  void sendData(float temp, float hum, PMS5003Data data) {
    if (WiFi.status() != WL_CONNECTED) {
      connectWiFi();
      return;
    }

    if (jwtToken == "") {
      if (!loginDevice()) return;
    }

    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", "Bearer " + jwtToken);

    StaticJsonDocument<200> doc;
    doc["device_id"] = device_id;
    doc["temperatura"] = temp;
    doc["humedad"] = hum;
    doc["pm1_0"] = data.pm10_standard;
    doc["pm2_5"] = data.pm25_standard;
    doc["pm10"] = data.pm100_standard;

    String payload;
    serializeJson(doc, payload);

    int code = http.POST(payload);
    Serial.printf("Server response: %d\n", code);

    if (code == 401 || code == 403) {
      jwtToken = "";
      Serial.println("⚠ Token expirado, reintentando login...");
      loginDevice();
    }

    http.end();
  }
};

// -------------------- APP --------------------
class AppController {
  SensorManager sensors;
  DisplayManager display;
  MyNetworkManager network;

  unsigned long lastSend = 0;
  unsigned long lastDisplay = 0;

public:
  AppController() : sensors(4, DHT22, Serial2) {}

  void setup() {
    Serial.begin(115200);
    network.connectWiFi();
    sensors.begin();
    display.begin();
    Serial.println("📡 Estación esp32n1 lista...");
  }

  void loop() {
    unsigned long now = millis();

    float temp = sensors.readTemp();
    float hum = sensors.readHum();
    PMS5003Data pms = sensors.readPMS();

    if (now - lastDisplay > 1000) {
      lastDisplay = now;
      display.showReadings(temp, hum, pms);
    }

    if (now - lastSend > 60000) {
      lastSend = now;
      network.sendData(temp, hum, pms);
    }
  }
};

AppController app;

void setup() { app.setup(); }
void loop() { app.loop(); }
