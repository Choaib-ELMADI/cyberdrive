const uint8_t ledPin = 5;

unsigned long currentMillis = 0;
unsigned long previousMillis = 0;
const long interval = 500;
bool ledState = LOW;

void setup() { pinMode(ledPin, OUTPUT); }

void loop() {
    currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis;

        if (ledState == LOW)
            ledState = HIGH;
        else
            ledState = LOW;

        digitalWrite(ledPin, ledState);
    }
}
