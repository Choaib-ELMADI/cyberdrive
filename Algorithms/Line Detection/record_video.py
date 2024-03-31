import cv2

# import numpy as np

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # type: ignore
out = cv2.VideoWriter("video__3.mp4", fourcc, 30.0, (640, 480))

while cap.isOpened():
    success, frame = cap.read()

    if success:
        out.write(frame)
        cv2.imshow("Image", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
