import cv2

image_name = "black_and_white.jpg"
image_path = f"C:\\Users\\Choaib ELMADI\\Downloads\\D.I.F.Y\\Electronics\\Robotics\\7- CyberDrive\\Assets\\Images\\{ image_name }"

bw_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

inverted_image = 255 - bw_image  # type: ignore

cv2.imshow("Image", bw_image)
cv2.imshow("Inverted Image", inverted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
