const uint8_t frontLight = 25;
const uint8_t brakeLight = 18;
const uint8_t rightBlinker = 19;
const uint8_t leftBlinker = 15;
const long frontLightInterval = 3000;
const long brakeLightInterval = 3000;
const long rightBlinkerInterval = 500;
const long leftBlinkerInterval = 500;
unsigned long previousMillisArray[4] = {0, 0, 0, 0};
bool ledStateArray[4] = {LOW, LOW, LOW, LOW};

void setup() {
    pinMode(frontLight, OUTPUT);
    pinMode(brakeLight, OUTPUT);
    pinMode(rightBlinker, OUTPUT);
    pinMode(leftBlinker, OUTPUT);
}

void loop() {
    blinkLED(frontLight, frontLightInterval, 0);
    blinkLED(brakeLight, brakeLightInterval, 1);
    blinkLED(rightBlinker, rightBlinkerInterval, 2);
    blinkLED(leftBlinker, leftBlinkerInterval, 3);
}

void blinkLED(uint8_t ledPin, long interval, uint8_t ledIndex) {
    if (millis() - previousMillisArray[ledIndex] >= interval) {
        previousMillisArray[ledIndex] = millis();

        if (ledStateArray[ledIndex] == LOW)
            ledStateArray[ledIndex] = HIGH;
        else
            ledStateArray[ledIndex] = LOW;

        digitalWrite(ledPin, ledStateArray[ledIndex]);
    }
}
