#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error "Bluetooth is not enabled!"
#endif

BluetoothSerial serialBT;
String data;
int steeringAngle;

// Motor A: RIGHT
const uint8_t ENA = 15;
const uint8_t IN1 = 2;
const uint8_t IN2 = 0;

// Motor B: LEFT
const uint8_t IN3 = 16;
const uint8_t IN4 = 4;
const uint8_t ENB = 17;

const int BASE_SPEED = 100;
const uint8_t CHANNEL_A = 0;
const uint8_t CHANNEL_B = 1;
const uint32_t FREQUENCY = 2000;
const uint8_t RESOLUTION_BITS = 8;

void setup() {
    Serial.begin(115200);
    serialBT.begin("ESP32 BT Communication");
    Serial.println("The device started, now you can pair it via Bluetooth.");

    pinMode(ENA, OUTPUT);
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(ENB, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);

    ledcSetup(CHANNEL_A, FREQUENCY, RESOLUTION_BITS);
    ledcAttachPin(ENA, CHANNEL_A);
    ledcSetup(CHANNEL_B, FREQUENCY, RESOLUTION_BITS);
    ledcAttachPin(ENB, CHANNEL_B);
}

void loop() {
    if (serialBT.available()) {
        data = serialBT.readStringUntil('\n');
    }

    int state = sscanf(data.c_str(), "%d", &steeringAngle);
    if (state == 1) {
        Serial.print("Steering angle: ");
        Serial.println(steeringAngle);

        switch (steeringAngle) {
        case 1:
            goForward(100);
            break;
        case 2:
            goBackward(100);
            break;
        case 3:
            left();
            break;
        case 4:
            right();
            break;
        case 5:
            goForward(160);
            break;
        case 6:
            goBackward(160);
            break;
        default:
            stop();
            break;
        }
    }
}

void goForward(uint8_t speed) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    ledcWrite(CHANNEL_A, speed);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    ledcWrite(CHANNEL_B, speed);
}

void goBackward(uint8_t speed) {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    ledcWrite(CHANNEL_A, speed);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    ledcWrite(CHANNEL_B, speed);
}

void left() {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    ledcWrite(CHANNEL_A, BASE_SPEED);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
}

void right() {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    ledcWrite(CHANNEL_B, BASE_SPEED);
}

void stop() {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
}
