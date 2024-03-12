import cv2
import numpy as np


video_name = "white.mp4"
video_path = f"C:\\Users\\Choaib ELMADI\\Downloads\\D.I.F.Y\\Electronics\\Robotics\\7- Mini Tesla\\Lines Detection\\Videos\\{ video_name }"


def empty(a):
    pass


cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 620, 230)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)  # type: ignore
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)  # type: ignore
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)  # type: ignore
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)  # type: ignore
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)  # type: ignore
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)  # type: ignore

cap = cv2.VideoCapture(video_path)

frame_counter = 0
while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, (480, 360))
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    frame_counter += 1
    if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frame_counter:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frame_counter = 0

    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv_image, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    h_stack = np.hstack([frame, mask, result])
    cv2.imshow("Horizontal Stacking", h_stack)

    if cv2.waitKey(1) and 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
