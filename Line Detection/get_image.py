import cv2
import matplotlib.pyplot as plt

video_name = "5.mp4"
WIDTH = 640
HEIGHT = 352

video_path = f"C:\\Users\\Choaib ELMADI\\Downloads\\D.I.F.Y\\Electronics\\Robotics\\7- CyberDrive\\Assets\\Videos\\{ video_name }"
cap = cv2.VideoCapture(video_path)

while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    plt.imshow(frame)
    plt.show()
