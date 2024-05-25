import cv2
import numpy as np
import matplotlib.pyplot as plt
import utils


video_name = "phone__video__2.mp4"
video_path = f"C:\\Users\\Choaib ELMADI\\Downloads\\D.I.F.Y\\Electronics\\Robotics\\7- CyberDrive\\Assets\\Videos\\{ video_name }"
# video_path = "http://192.168.88.202:81/stream"

global curves_list
curves_list = []
max_curves_list_len = 5
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
text_background = (198, 63, 88)
corner_color = (53, 53, 249)
text_color = (239, 239, 239)
border_color = (61, 147, 8)


def get_image_curve(image, show=2):
    global curves_list
    image_copy = np.copy(image)

    thresholded_image = utils.threshold_image(image)

    height, width, _ = image.shape
    points = np.float32([[100, 180], [400, 180], [width - 10, height - 10], [10, height - 10]])  # type: ignore
    warped_image = utils.warp_image(thresholded_image, points, width, height)

    image_with_points = utils.draw_points(np.copy(image), points)

    mid_point, _ = utils.pixel_summation(warped_image, percent=0.2, show=True, region=2)
    base_point, summation_image = utils.pixel_summation(
        warped_image, percent=0.4, show=True
    )
    raw_curve = base_point - mid_point

    curves_list.append(raw_curve)
    if len(curves_list) > max_curves_list_len:
        curves_list = curves_list[-max_curves_list_len:]
    curve = int(np.average(curves_list))

    warped_image_inv = utils.warp_image(
        thresholded_image, points, width, height, inv=True
    )
    warped_image_inv[0 : image.shape[0], 0 : image.shape[1]] = (
        warped_image_inv[0 : image.shape[0], 0 : image.shape[1]] & GREEN
    )
    warped_image_inv[0:240, 0 : image.shape[1]] = (
        warped_image_inv[0:240, 0 : image.shape[1]] & BLACK
    )
    result_image = cv2.addWeighted(image_copy, 0.7, warped_image_inv, 1, 0)

    str_curve = str(curve)
    right_distance = image.shape[1] // 2
    if len(str_curve) == 3:
        right_distance = image.shape[1] // 2 - 60
    elif len(str_curve) == 2:
        right_distance = image.shape[1] // 2 - 30
    cv2.putText(
        result_image,
        str_curve,
        (right_distance, 85),
        cv2.FONT_HERSHEY_COMPLEX_SMALL,
        2,
        text_color,
        3,
    )

    cv2.rectangle(
        result_image,
        (0, image.shape[0] - 14),
        (image.shape[1], image.shape[0]),
        text_color,
        cv2.FILLED,
    )
    for x in range(-30, 30):
        w = image.shape[1] // 20
        cv2.line(
            result_image,
            (w * x + int(curve // 50), image.shape[0] - 13),
            (w * x + int(curve // 50), image.shape[0] - 1),
            text_background,
            2,
        )

    cv2.line(
        result_image,
        (image.shape[1] // 2, image.shape[0] - 6),
        (image.shape[1] // 2 + (curve * 3), image.shape[0] - 6),
        corner_color,
        2,
    )
    cv2.line(
        result_image,
        ((image.shape[1] // 2 + (curve * 3)), image.shape[0] - 13),
        (image.shape[1] // 2 + (curve * 3), image.shape[0] - 1),
        corner_color,
        6,
    )
    cv2.circle(
        result_image,
        (image.shape[1] // 2, image.shape[0] - 6),
        4,
        corner_color,
        cv2.FILLED,
    )

    if show == 2:
        stacked_images = utils.stack_images(
            0.7,
            (
                [image, image_with_points, warped_image],
                [summation_image, warped_image_inv, result_image],
            ),
        )
        cv2.imshow("Stacked Images: Pipeline", stacked_images)
    elif show == 1:
        cv2.imshow("Result Image", result_image)

    return curve


if __name__ == "__main__":
    cap = cv2.VideoCapture(video_path)

    frame_counter = 0
    while True:
        _, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))

        curve = get_image_curve(frame, show=2)
        # curve = get_image_curve(frame)
        print(curve)

        # plt.imshow(frame)
        # plt.show()

        frame_counter += 1
        if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            frame_counter = 0
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
