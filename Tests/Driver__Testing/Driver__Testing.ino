// Motor A: RIGHT
const uint8_t ENA = 15;
const uint8_t IN1 = 2;
const uint8_t IN2 = 0;

// Motor B: LEFT
const uint8_t ENB = 4;
const uint8_t IN3 = 16;
const uint8_t IN4 = 17;

const int BASE_SPEED = 100;
const uint8_t CHANNEL_A = 0;
const uint8_t CHANNEL_B = 1;
const uint32_t FREQUENCY = 2000;
const uint8_t RESOLUTION_BITS = 8;

void setup() {
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
    goForward(80);
    delay(3000);
    goForward(120);
    delay(3000);
    goForward(255);
    delay(3000);
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
