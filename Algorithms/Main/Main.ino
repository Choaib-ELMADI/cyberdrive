// Video Stream
#include "camera_pins.h"
#include "esp_camera.h"
#include <WiFi.h>
// Video Stream END

// Bluetooth Communication
#include "BluetoothSerial.h"
// Bluetooth Communication END

// Video Stream
const char *ssid = "Choaibs-Phone";
const char *password = "devchoaib";
// Video Stream END

// Bluetooth Communication
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error "Bluetooth is not enabled!"
#endif

BluetoothSerial serialBT;
String data;
int v1, v2, v3;
int number;
// Bluetooth Communication END

TaskHandle_t Task1_with_WiFi;
TaskHandle_t Task2_with_Bluetooth;

void createTasks();
void Task1(void *);
void Task2(void *);

void setupCamera();
camera_config_t setupConfiguration();

void connectToWiFi();

void startCameraServer();

void communicationFunction();

void setup() {
    Serial.begin(115200);
    serialBT.begin("ESP32-CAM__BT");
    Serial.println("The device started, now you can pair it via Bluetooth.");

    createTasks();

    setupCamera();

    connectToWiFi();
}

void loop() {}

void createTasks() {
    xTaskCreatePinnedToCore(Task1, "Task1", 10000, NULL, 1, &Task1_with_WiFi,
                            0);
    delay(500);
    xTaskCreatePinnedToCore(Task2, "Task2", 10000, NULL, 1,
                            &Task2_with_Bluetooth, 1);
    delay(500);
}
void Task1(void *pvParameters) { startCameraServer(); }
void Task2(void *pvParameters) {
    for (;;) {
        communicationFunction();
    }
}

void setupCamera() {
    camera_config_t config = setupConfiguration();

    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK) {
        Serial.printf("Camera init failed with error 0x%x", err);
        return;
    }

    sensor_t *s = esp_camera_sensor_get();
    s->set_framesize(s, FRAMESIZE_VGA);
}
camera_config_t setupConfiguration() {
    camera_config_t config;

    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sccb_sda = SIOD_GPIO_NUM;
    config.pin_sccb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 10000000;
    config.frame_size = FRAMESIZE_VGA;
    config.pixel_format = PIXFORMAT_JPEG;
    config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
    config.fb_location = CAMERA_FB_IN_PSRAM;
    config.jpeg_quality = 16;
    config.fb_count = 1;

    return config;
}

void connectToWiFi() {
    WiFi.begin(ssid, password);
    WiFi.setSleep(false);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi connected");

    // startCameraServer();

    Serial.print("Camera Ready! Use 'http://");
    Serial.print(WiFi.localIP());
    Serial.println("' to connect");
}

void communicationFunction() {
    // Send Data
    number = random(100);
    if (serialBT.available()) {
        serialBT.println(number);
    }

    // Receive Data
    if (serialBT.available()) {
        data = serialBT.readStringUntil('\n');
        sscanf(data.c_str(), "%d, %d, %d", &v1, &v2, &v3);

        Serial.print(v1);
        Serial.print(" - ");
        Serial.print(v2);
        Serial.print(" - ");
        Serial.println(v3);
    }

    delay(20);
}
