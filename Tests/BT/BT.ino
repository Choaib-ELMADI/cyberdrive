#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error "Bluetooth is not enabled!"
#endif

BluetoothSerial serialBT;
char data[20] = "";
char cmd[3] = "";

void setup() {
    Serial.begin(115200);
    serialBT.begin("ESP32-CAM__BT");
    Serial.println("The device started, now you can pair it via Bluetooth.");
}

void loop() {
    // => Send data from PC to the connected device
    // if (Serial.available()) {
    //     serialBT.write(Serial.read());
    // }

    // => Receive data from the connected device
    // if (serialBT.available()) {
    //     Serial.write(serialBT.read());
    // }

    if (serialBT.available()) {
        data = serialBT.read();
        Serial.println(data);
    }

    if (serialBT.available()) {
        cmd = Serial.read();
        serialBT.write(cmd);
    }

    delay(20);
}