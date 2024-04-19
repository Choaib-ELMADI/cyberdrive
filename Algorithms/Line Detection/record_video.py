import cv2

stream = "http://192.168.88.202:81/stream"
# stream = 0
fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")  # type: ignore
fps = 25.0
# fps = 30.0

cap = cv2.VideoCapture(stream)
writer = cv2.VideoWriter("rec__8.mp4", fourcc, fps, (640, 480))

while True:
    ret, frame = cap.read()

    if ret:
        cv2.imshow("Image", frame)
        writer.write(frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
writer.release()
cv2.destroyAllWindows()
