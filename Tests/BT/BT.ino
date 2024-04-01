#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error "Bluetooth is not enabled!"
#endif

BluetoothSerial serialBT;
String data;
int v1, v2, v3;
int number;

void setup() {
    Serial.begin(115200);
    serialBT.begin("ESP32-CAM__BT");
    Serial.println("The device started, now you can pair it via Bluetooth.");
}

void loop() {
    // Send Data
    number = random(100);
    if (serialBT.available()) {
        serialBT.println(number);
    }

    // Receive Data
    if (serialBT.available()) {
        data = serialBT.readStringUntil('\n');
        sscanf(data.c_str(), "%d, %d, %d", &v1, &v2, &v3);

        Serial.print(v1);
        Serial.print(" - ");
        Serial.print(v2);
        Serial.print(" - ");
        Serial.println(v3);
    }

    delay(100);
}