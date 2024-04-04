// Motor A: RIGHT
const uint8_t ENA = 15;
const uint8_t IN1 = 2;
const uint8_t IN2 = 0;

// Motor B: LEFT
const uint8_t ENB = 4;
const uint8_t IN3 = 16;
const uint8_t IN4 = 17;

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
    goForward();
    delay(3000);

    goBackward();
    delay(3000);

    left();
    delay(1000);

    right();
    delay(1000);
}

void goForward() {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, BASE_SPEED);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, BASE_SPEED);
}

void goBackward() {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    analogWrite(ENA, BASE_SPEED);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENB, BASE_SPEED);
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
