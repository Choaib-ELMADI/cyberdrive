const uint8_t trig = 14;
const uint8_t echo = 27;
const uint8_t trigHighDelay = 10;
const uint8_t trigLowDelay = 2;

void setup() {
    Serial.begin(9600);

    pinMode(trig, OUTPUT);
    pinMode(echo, INPUT);
}

void loop() {
    int distance = obstacleDistance(trig, echo);
    Serial.println(distance);
    // delay(250);
}

int obstacleDistance(int trig, int echo) {
    static unsigned long prevTrigLowTime = 0;
    static unsigned long prevTrigHighTime = 0;

    int distance, duration;

    if (micros() - prevTrigLowTime < trigLowDelay) {
        digitalWrite(trig, LOW);
        prevTrigLowTime = micros();
    }

    if (micros() - prevTrigHighTime > trigHighDelay) {
        digitalWrite(trig, HIGH);
        prevTrigHighTime = micros();
    }
    digitalWrite(trig, LOW);

    duration = pulseIn(echo, HIGH);
    distance = duration * 0.034 / 2;

    return distance;
}