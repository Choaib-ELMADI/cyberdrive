import cv2
import math
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cvzone

detector = HandDetector(detectionCon=0.5, maxHands=1)

raw_distance = [
    300,
    245,
    200,
    170,
    145,
    130,
    112,
    103,
    93,
    87,
    80,
    75,
    70,
    67,
    62,
    59,
    57,
]
act_distance = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
A, B, C = np.polyfit(raw_distance, act_distance, 2)
A, B, C = round(float(A), 3), round(float(B), 3), round(float(C), 3)

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    hands, _ = detector.findHands(frame, draw=False)
    if hands:
        lm_list = hands[0]["lmList"]
        x, y, w, h = hands[0]["bbox"]
        x1, y1, _ = lm_list[5]
        x2, y2, __ = lm_list[17]

        distance = int(math.sqrt(pow(y2 - y1, 2) + pow(x2 - x1, 2)))
        cm_distance = int(A * pow(distance, 2) + B * distance + C - 10)
        cvzone.putTextRect(
            frame,
            f"{ distance }px, { cm_distance }cm",
            (x + 7, y - 16),
            thickness=1,
            scale=1,
            font=cv2.FONT_HERSHEY_COMPLEX_SMALL,
            colorR=(0, 0, 0),
        )
        cvzone.cornerRect(frame, (x, y, w, h), colorR=(0, 0, 0))

    cv2.imshow("Image", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
