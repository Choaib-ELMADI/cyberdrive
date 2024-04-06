#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "Wire.h"

#include "BluetoothSerial.h"
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error "Bluetooth is not enabled!"
#endif

#define INTERRUPT_PIN 34

MPU6050 mpu;
bool dmpReady;
uint8_t devStatus;
uint8_t fifoBuffer[64];
Quaternion q;
VectorFloat gravity;
float ypr[3], yawPitchRoll[3];
volatile bool mpuInterrupt;

BluetoothSerial serialBT;
String data;
int steeringAngle;

unsigned long previousMillisTime = 0;
const uint8_t delayMillisTime = 200;

const uint8_t ENA = 32;
const uint8_t IN1 = 2;
const uint8_t IN2 = 0;
const uint8_t IN3 = 16;
const uint8_t IN4 = 4;
const uint8_t ENB = 17;
const uint8_t motorsPins[6] = {ENA, IN1, IN2, IN3, IN4, ENB};

const int BASE_SPEED = 100;
const uint8_t CHANNEL_A = 0;
const uint8_t CHANNEL_B = 1;
const uint32_t FREQUENCY = 2000;
const uint8_t RESOLUTION_BITS = 8;

const uint8_t trigHighDelay = 10;
const uint8_t trigLowDelay = 2;
const uint8_t triggerPin = 14;
const uint8_t echoPin = 27;
int objectDistance;

void setup() {
    Serial.begin(115200);

    // MPU6050 Setup
    Wire.begin();
    Wire.setClock(400000);
    initializeMPU();

    // Bluetooth Setup
    serialBT.begin("ESP32 BT Communication");
    Serial.println("The device started, now you can pair it via Bluetooth.");

    // Motors Setup
    for (uint8_t i = 0; i < 6; ++i) {
        pinMode(motorsPins[i], OUTPUT);
    }
    for (uint8_t i = 1; i < 5; ++i) {
        digitalWrite(motorsPins[i], LOW);
    }
    ledcSetup(CHANNEL_A, FREQUENCY, RESOLUTION_BITS);
    ledcAttachPin(ENA, CHANNEL_A);
    ledcSetup(CHANNEL_B, FREQUENCY, RESOLUTION_BITS);
    ledcAttachPin(ENB, CHANNEL_B);
}

void loop() {
    if (serialBT.available()) {
        data = serialBT.readStringUntil('\n');
    }

    // if (millis() - previousMillisTime >= delayMillisTime) {
    // previousMillisTime = millis();

    float *yprAngles = getYawPitchRoll();
    Serial.print("Yaw: ");
    Serial.print(yprAngles[0]);
    Serial.print(" ");

    objectDistance = obstacleDistance(triggerPin, echoPin);
    Serial.print("Distance: ");
    Serial.print(objectDistance);
    Serial.print("cm ");

    int state = sscanf(data.c_str(), "%d", &steeringAngle);
    if (state == 1) {
        Serial.print("Steering angle: ");
        Serial.print(steeringAngle);
        Serial.print(" ");

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

    Serial.println("");
    // }
}

/* ******************
 * MPU6050 FUNCTIONS *
 ****************** */
void dmpDataReady() { mpuInterrupt = true; }
void initializeMPU() {
    mpu.initialize();
    pinMode(INTERRUPT_PIN, INPUT);
    if (mpu.testConnection()) {
        Serial.println("MPU6050 connection successful.");
    } else {
        Serial.println("MPU6050 connection failed.");
    }

    Serial.println("Initializing DMP...");
    devStatus = mpu.dmpInitialize();

    mpu.setXGyroOffset(220);
    mpu.setYGyroOffset(76);
    mpu.setZGyroOffset(-85);
    mpu.setZAccelOffset(1788);

    if (devStatus == 0) {
        mpu.CalibrateAccel(6);
        mpu.CalibrateGyro(6);
        mpu.PrintActiveOffsets();
        mpu.setDMPEnabled(true);

        attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), dmpDataReady,
                        RISING);

        Serial.println(F("DMP ready! Waiting for first interrupt..."));
        dmpReady = true;
    } else {
        Serial.println("DMP Initialization failed.");
    }
}
float *getYawPitchRoll() {
    if (dmpReady) {
        if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) {
            mpu.dmpGetQuaternion(&q, fifoBuffer);
            mpu.dmpGetGravity(&gravity, &q);
            mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
            for (int i = 0; i < 3; ++i) {
                yawPitchRoll[i] = ypr[i] * 180 / M_PI;
            }

            return yawPitchRoll;
        }
    }
}

/* *****************
 * L298N FUNCTIONS *
 ***************** */
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

/* *******************
 * HC-SR04 FUNCTIONS *
 ******************* */
int obstacleDistance(uint8_t trig, uint8_t echo) {
    // // unsigned long prevTrigLowTime = 0;
    // // unsigned long prevTrigHighTime = 0;
    // int distance, duration;

    // // if (micros() - prevTrigLowTime < trigLowDelay) {
    // digitalWrite(trig, LOW);
    // delayMicroseconds(trigLowDelay);
    // //     prevTrigLowTime = micros();
    // // }
    // // if (micros() - prevTrigHighTime > trigHighDelay) {
    // digitalWrite(trig, HIGH);
    // delayMicroseconds(trigHighDelay);
    // //     prevTrigHighTime = micros();
    // // }
    // digitalWrite(trig, LOW);

    // duration = pulseIn(echo, HIGH);
    // distance = duration * 0.034 / 2;

    return 25;
}
