import cv2

video_path = "http://192.168.88.202:81/stream"

cap = cv2.VideoCapture(video_path)

while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
