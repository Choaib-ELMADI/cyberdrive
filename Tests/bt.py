import time
import serial
import random

print("Connecting BT...")
bluetooth = serial.Serial(port="COM5", baudrate=115200, timeout=0)
print("BT connected.")

while True:
    # steering_angle = random.randint(10, 99)
    steering_angle = int(input("Enter an angle: "))
    bluetooth.write(f"{steering_angle}\n".encode())
