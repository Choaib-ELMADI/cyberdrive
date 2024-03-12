import cv2
import math

image_name = "angles.jpg"
image_path = f"C:\\Users\\Choaib ELMADI\\Downloads\\D.I.F.Y\\Electronics\\Robotics\\7- Mini Tesla\\Angle Detection\\{image_name}"
image = cv2.imread(image_path)

points_list = []


def handle_mouse_click(event, x, y, _, __):
    if event == cv2.EVENT_LBUTTONDOWN:
        size = len(points_list)
        if size and size % 3:
            cv2.line(
                image,
                points_list[-1],
                (x, y),
                (0, 0, 255),
                3,
                0,
            )

        cv2.circle(image, (x, y), 4, (0, 0, 255), cv2.FILLED)
        points_list.append([x, y])


def slope(p1, p2):
    if p2[0] == p1[0]:
        return -999

    return (p2[1] - p1[1]) / (p2[0] - p1[0])


def get_angle():
    left_point, head, right_point = points_list[-3:]
    s1 = slope(head, right_point)
    s2 = slope(head, left_point)

    radians_angle = math.atan((s1 - s2) / (1 + s1 * s2))
    degree_angle = round(math.degrees(radians_angle))

    return degree_angle


while True:
    cv2.imshow("Image", image)
    cv2.setMouseCallback("Image", handle_mouse_click)  # type: ignore

    size = len(points_list)
    if size and not (size % 3):
        angle = get_angle()
        print(angle)

    if cv2.waitKey(1) & 0xFF == ord("c"):
        points_list = []
        image = cv2.imread(image_path)
