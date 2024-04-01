import serial
import random

print("Connecting BT...")
bluetooth = serial.Serial(port="COM4", baudrate=115200, timeout=0)
print("BT connected.")

while True:
    # Receive Data
    if bluetooth.in_waiting > 0:
        data = bluetooth.readline().decode().strip()
        print(data)

    # Send Data
    v1 = random.randint(0, 10)
    v2 = random.randint(10, 20)
    v3 = random.randint(20, 30)
    bluetooth.write(f"{v1}, {v2}, {v3}\n".encode())
