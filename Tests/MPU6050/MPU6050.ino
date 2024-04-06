#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "Wire.h"

#define INTERRUPT_PIN 34

MPU6050 mpu;
bool dmpReady;
uint8_t devStatus;
uint8_t fifoBuffer[64];
Quaternion q;
VectorFloat gravity;
float ypr[3], yawPitchRoll[3];
volatile bool mpuInterrupt;

void setup() {
    Serial.begin(115200);
    Wire.begin();
    Wire.setClock(400000);

    initializeMPU();
}

void loop() {
    float *yprAngles = getYawPitchRoll();
    Serial.print("Yaw: ");
    Serial.println(yprAngles[0]);
}

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
