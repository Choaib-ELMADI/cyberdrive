import time

delay = 2
start_time = time.time()

while True:
    while time.time() - start_time < delay:
        # print("Hi")
        pass

    start_time = time.time()
    print("Hello")
