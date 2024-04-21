import cv2
from utils import *

video_name = "rec__2__2.mp4"
video_path = f"C:\\Users\\Choaib ELMADI\\Downloads\\D.I.F.Y\\Electronics\\Robotics\\7- CyberDrive\\Assets\\Videos\\{ video_name }"

cap = cv2.VideoCapture(video_path)

frame_counter = 0
while True:
    _, frame = cap.read()
    # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresholded_frame = threshold_image(frame)

    cv2.imshow("Frame", frame)
    # cv2.imshow("Gray Frame", gray_frame)
    cv2.imshow("Thresholded Frame", thresholded_frame)

    frame_counter += 1
    if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        frame_counter = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
