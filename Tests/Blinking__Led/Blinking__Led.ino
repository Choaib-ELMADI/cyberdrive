const uint8_t redLED = 5;
const uint8_t greenLED = 4;
const uint8_t yellowLED = 3;
const long redInterval = 500;
const long greenInterval = 1000;
const long yellowInterval = 500;
unsigned long previousMillisArray[3] = {0, 0, 0};
bool ledStateArray[3] = {LOW, LOW, LOW};

void setup() {
    pinMode(redLED, OUTPUT);
    pinMode(greenLED, OUTPUT);
    pinMode(yellowLED, OUTPUT);
}

void loop() {
    blinkLED(redLED, redInterval, 0);
    blinkLED(greenLED, greenInterval, 1);
    blinkLED(yellowLED, yellowInterval, 2);
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
