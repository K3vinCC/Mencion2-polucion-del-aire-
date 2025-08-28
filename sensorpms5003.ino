
                          #include "PMS.h"

// PMS5003 en UART2 (GPIO16 = RX, GPIO17 = TX)
HardwareSerial pmsSerial(2);
PMS pms(pmsSerial);
PMS::DATA data;

void setup() {
  Serial.begin(115200);
  pmsSerial.begin(9600, SERIAL_8N1, 16, 17); // RX=16, TX=17
  Serial.println("Iniciando PMS5003...");
}

void loop() {
  if (pms.read(data)) {
    Serial.print("PM1.0: ");
    Serial.print(data.PM_AE_UG_1_0);
    Serial.print("  PM2.5: ");
    Serial.print(data.PM_AE_UG_2_5);
    Serial.print("  PM10: ");
    Serial.println(data.PM_AE_UG_10_0);
  }
}
