import cv2
import numpy as np


def handle_mouse_click(event, x, y, _, __):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"({ x }, { y })")


image_name = "cards__1.webp"
image_path = f"C:\\Users\\Choaib ELMADI\\Downloads\\D.I.F.Y\\Electronics\\Robotics\\7- CyberDrive\\Assets\\Images\\{ image_name }"
image = cv2.imread(image_path)
image = cv2.resize(image, (900, 557))

width, height = 250, 350
pts1 = np.float32([[522, 41], [711, 54], [865, 324], [555, 314]])  # type: ignore
pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])  # type: ignore

matrix = cv2.getPerspectiveTransform(
    pts1,  # type: ignore
    pts2,  # type: ignore
)
result = cv2.warpPerspective(image, matrix, (width, height))

for i in range(4):
    cv2.circle(image, (int(pts1[i][0]), int(pts1[i][1])), 4, (0, 0, 255), cv2.FILLED)  # type: ignore

cv2.imshow("Image", image)
cv2.imshow("Result", result)
cv2.waitKey(0)

"""
while True:
    cv2.imshow("Image", image)
    cv2.setMouseCallback("Image", handle_mouse_click)  # type: ignore
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
"""
