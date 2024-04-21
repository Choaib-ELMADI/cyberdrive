import cv2
import numpy as np


def threshold_image(image):
    # WHITE
    lower_white = np.array([0, 0, 158])
    upper_white = np.array([179, 255, 255])

    # BLACK
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([179, 255, 179])  # 3rd: 150 --> 180

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # white_mask = cv2.inRange(hsv_image, lower_white, upper_white)
    black_mask = cv2.inRange(hsv_image, lower_black, upper_black)
    white_mask = np.ones_like(black_mask, dtype=np.uint8) * 255
    white_mask = white_mask - black_mask  # type: ignore
    # white_mask = not black_mask
    thresholded_image = cv2.bitwise_and(image, image, mask=white_mask)

    return thresholded_image
