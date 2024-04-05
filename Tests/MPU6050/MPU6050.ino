#include "mpu_setup.cpp"

void initializeMPU();
float *getYawPitchRoll();

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
