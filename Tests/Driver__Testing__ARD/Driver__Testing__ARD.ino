// Motor A: RIGHT
const uint8_t ENA = 3;
const uint8_t IN1 = 4;
const uint8_t IN2 = 5;

// Motor B: LEFT
const uint8_t IN3 = 7;
const uint8_t IN4 = 6;
const uint8_t ENB = 9;

const int BASE_SPEED = 100;

void setup() {
    pinMode(ENA, OUTPUT);
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(ENB, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
}

void loop() {
    goForward(120);
    delay(3000);

    goBackward(120);
    delay(3000);

    left();
    delay(1500);

    right();
    delay(1500);
}

void goForward(uint8_t speed) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, speed);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, speed);
}

void goBackward(uint8_t speed) {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    analogWrite(ENA, speed);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENB, speed);
}

void left() {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, BASE_SPEED);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
}

void right() {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, BASE_SPEED);
}
