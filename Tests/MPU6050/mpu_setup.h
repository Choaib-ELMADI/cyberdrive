#ifndef MPU_SETUP_H
#define MPU_SETUP_H

#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "Wire.h"

#define INTERRUPT_PIN 2

MPU6050 mpu;
bool dmpReady = false;
uint8_t devStatus;
uint8_t fifoBuffer[64];
Quaternion q;
VectorFloat gravity;
float ypr[3], yawPitchRoll[3];
volatile bool mpuInterrupt = false;

#endif // MPU_SETUP_H
