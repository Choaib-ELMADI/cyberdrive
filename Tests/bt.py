import serial

print("Connecting BT...")
bluetooth = serial.Serial(port="COM4", baudrate=115200, timeout=0)
print("BT connected.")

while True:
    if bluetooth.in_waiting > 0:
        data = bluetooth.readline()
        print(data)

    bluetooth.write(("3").encode("utf-8"))
