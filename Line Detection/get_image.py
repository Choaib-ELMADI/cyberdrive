import cv2
import matplotlib.pyplot as plt

video = 5
WIDTH = 640
HEIGHT = 352

video_path = f"C:\\Users\\Choaib ELMADI\\Downloads\\D.I.F.Y\\Electronics\\Robotics\\7- Mini Tesla\\Lines Detection\\Videos\\{ video }.mp4"
cap = cv2.VideoCapture(video_path)

while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    plt.imshow(frame)
    plt.show()
