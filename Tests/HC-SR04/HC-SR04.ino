const uint8_t frontTrig = 12;
const uint8_t frontEcho = 11;

int trigHighDelay = 10;
int trigLowDelay = 2;

void setup() {
    Serial.begin(9600);

    pinMode(frontTrig, OUTPUT);
    pinMode(frontEcho, INPUT);
}

void loop() {
    int front = obstacleDistance(frontTrig, frontEcho);
    Serial.println(front);
}

int obstacleDistance(int trig, int echo) {
    unsigned long prevTrigLowTime = 0;
    unsigned long prevTrigHighTime = 0;

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