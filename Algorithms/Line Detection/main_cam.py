import cv2
import numpy as np

video_name = "6.mp4"
WIDTH = 640
HEIGHT = 352
SELECTION = [
    {
        "width": 640,
        "height": 352,
        "top": (280, 125),
        "left": (100, HEIGHT),
        "right": (550, HEIGHT),
    },
    {
        "width": 405,
        "height": 720,
        "top": (235, 465),
        "left": (0, 600),
        "right": (WIDTH, 544),
    },
    {
        "width": 405,
        "height": 720,
        "top": (190, 480),
        "left": (75, HEIGHT),
        "right": (380, HEIGHT),
    },
    {
        "width": 640,
        "height": 352,
        "top": (300, 200),
        "left": (100, HEIGHT),
        "right": (500, HEIGHT),
    },
    {
        "width": 640,
        "height": 352,
        "top": (326, 223),
        "left": (100, HEIGHT),
        "right": (580, HEIGHT),
    },
    {
        "width": 640,
        "height": 352,
        "top": (330, 180),
        "left": (0, 300),
        "right": (WIDTH, 300),
    },
    {
        "width": 640,
        "height": 352,
        "top": (335, 100),
        "left": (0, 300),
        "right": (WIDTH, HEIGHT),
    },
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
    top = SELECTION[video]["top"]
    left = SELECTION[video]["left"]
    right = SELECTION[video]["right"]
    triangles = np.array([[left, right, top]], dtype=np.int32)

    mask = np.zeros_like(image)
    cv2.fillPoly(mask, triangles, 255)  # type: ignore
    masked_image = cv2.bitwise_and(image, mask)

    return masked_image


def display_lines(image, lines, color=(255, 0, 0)):
    lines_image = np.zeros_like(image)

    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(lines_image, (x1, y1), (x2, y2), color, 5)
            # print(f"Line: ({ x1 }, { y1 }), ({ x2 }, { y2 })")

    return lines_image


def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            x1 = min(x1, image.shape[1])
            x2 = min(x2, image.shape[1])
            y1 = min(y1, image.shape[0])
            y2 = min(y2, image.shape[0])

            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]

            if slope < 0:
                left_fit.append((slope, intercept))

            if slope > 0:
                right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)

    return np.array([left_line, right_line])


def make_coordinates(image, line_params):
    try:
        slope, intercept = line_params
    except TypeError:
        slope, intercept = 0.0001, 0

    y1 = image.shape[0]
    # y2 = 500
    y2 = SELECTION[video]["top"][1] + 50
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    return np.array([x1, y1, x2, y2])


video_path = f"C:\\Users\\Choaib ELMADI\\Downloads\\D.I.F.Y\\Electronics\\Robotics\\7- CyberDrive\\Assets\\Videos\\{ video_name }"
cap = cv2.VideoCapture(video_path)

frame_counter = 0
while cap.isOpened():
    _, frame = cap.read()
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    frame_counter += 1

    if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        frame_counter = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    canny_image = canny(frame)
    masked_image = region_of_interest(canny_image)

    lines = cv2.HoughLinesP(
        masked_image,
        2,
        np.pi / 180,
        100,
        np.array([]),
        minLineLength=40,
        maxLineGap=5_000,
    )
    averaged_lines = average_slope_intercept(frame, lines)
    lines_image = display_lines(frame, averaged_lines)
    # lines_image = display_lines(frame, lines)

    result_image = cv2.addWeighted(frame, 0.6, lines_image, 1, 1)
    cv2.imshow("Result Image", result_image)
    cv2.imshow("Original Image", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
