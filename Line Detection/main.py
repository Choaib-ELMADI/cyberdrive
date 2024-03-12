import cv2
import numpy as np
import random

WIDTH = 640
HEIGHT = 352
COLORS = [
    {"color": (0, 0, 255), "name": "RED"},
    {"color": (0, 255, 0), "name": "GREEN"},
    {"color": (255, 0, 0), "name": "BLUE"},
    {"color": (0, 255, 255), "name": "YELLOW"},
    {"color": (255, 255, 0), "name": "TEAL"},
    {"color": (255, 0, 255), "name": "VIOLET"},
]


def canny(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    canny_image = cv2.Canny(blur_image, 50, 150)

    # cv2.imshow("Gray Image", gray_image)
    # cv2.imshow("Blur Image", blur_image)
    # cv2.imshow("Canny Image", canny_image)

    return canny_image


def region_of_interest(image):
    top = (280, 125)
    left = (100, HEIGHT)
    right = (550, HEIGHT)
    triangles = np.array([[left, right, top]], dtype=np.int32)

    mask = np.zeros_like(image)
    cv2.fillPoly(mask, triangles, 255)  # type: ignore
    masked_image = cv2.bitwise_and(image, mask)

    return masked_image


def display_lines(image, lines):
    lines_image = np.zeros_like(image)

    if lines is not None:
        for line in lines:
            index = random.randint(0, 5)
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(lines_image, (x1, y1), (x2, y2), COLORS[index]["color"], 5)
            print(x1, y1, x2, y2, " COLOR: ", COLORS[index]["name"])

    return lines_image


def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]

            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)

    return np.array([left_line, right_line])


def make_coordinates(image, line_params):
    slope, intercept = line_params

    y1 = image.shape[0]
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    return np.array([x1, y1, x2, y2])


image_name = "1.jpg"
image_path = f"C:\\Users\\Choaib ELMADI\\Downloads\\D.I.F.Y\\Electronics\\Robotics\\7- Mini Tesla\\Lines Detection\\Images\\{ image_name }"
image = cv2.imread(image_path)
image = cv2.resize(image, (WIDTH, HEIGHT))
lane_image = np.copy(image)

canny_image = canny(lane_image)
# cv2.imshow("Canny Image", canny_image)

masked_image = region_of_interest(canny_image)
# cv2.imshow("Masked Image", masked_image)

lines = cv2.HoughLinesP(
    masked_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5
)
averaged_lines = average_slope_intercept(lane_image, lines)
lines_image = display_lines(lane_image, averaged_lines)
# lines_image = display_lines(lane_image, lines)
# cv2.imshow("Lines Image", lines_image)

result_image = cv2.addWeighted(lane_image, 0.6, lines_image, 1, 1)
cv2.imshow("Result Image", result_image)
cv2.imwrite("result_img__4.jpg", result_image)
cv2.imwrite("original_img__4.jpg", image)

cv2.imshow("Original Image", image)
cv2.waitKey(0)
