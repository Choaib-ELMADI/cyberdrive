import requests
import random


def handle_steering_angle_update(steering_angle):
    url = "http://192.168.45.202/"
    params = {"steeringAngle": steering_angle}
    response = requests.put(url, params=params)
    if response.status_code == 200:
        print("Steering angle updated successfully")
    else:
        print("Failed to update steering angle")


while True:
    # Send Data
    steering_angle = random.randint(-60, 60)
    handle_steering_angle_update(steering_angle)
