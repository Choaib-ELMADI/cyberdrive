import cv2
import numpy as np


def threshold_image(image):
    # WHITE
    # lower_white = np.array([70, 0, 0])
    # upper_white = np.array([179, 255, 255])

    # WHITE
    lower_white = np.array([0, 0, 158])
    upper_white = np.array([179, 255, 255])

    # BLACK
    # lower_white = np.array([88, 14, 0])
    # upper_white = np.array([179, 232, 255])

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    white_mask = cv2.inRange(hsv_image, lower_white, upper_white)
    thresholded_image = cv2.bitwise_and(image, image, mask=white_mask)

    return thresholded_image


def warp_image(image, original_points, width, height, inv=False):
    pts1 = np.float32(original_points)
    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])  # type: ignore

    if inv:
        matrix = cv2.getPerspectiveTransform(pts2, pts2)  # type: ignore
    else:
        matrix = cv2.getPerspectiveTransform(pts1, pts2)  # type: ignore

    warped_image = cv2.warpPerspective(image, matrix, (width, height))

    return warped_image


def draw_points(image, points, color=(0, 0, 255)):
    for i in range(4):
        cv2.circle(image, (int(points[i][0]), int(points[i][1])), 6, color, cv2.FILLED)  # type: ignore

    return image


def pixel_summation(image, percent=0.1, show=False, region=1):
    image_copy = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if region == 1:
        summation_values = np.sum(image_copy, axis=0)
    else:
        summation_values = np.sum(
            image_copy[image_copy.shape[0] // region :, :], axis=0
        )

    max_summation = np.max(summation_values)
    min_summation = percent * max_summation

    indexes_array = np.where(summation_values >= min_summation)
    base_point = int(np.average(indexes_array))

    if show:
        summation_image = np.zeros(image.shape, np.uint8)
        for i, intensity in enumerate(summation_values):
            cv2.line(
                summation_image,
                (i, image.shape[0]),
                (i, image.shape[0] - (intensity // 200 // region)),
                (0, 0, 255),
            )

        cv2.circle(
            summation_image,
            (base_point, image.shape[0]),
            15,
            (255, 0, 0),
            cv2.FILLED,
        )

        return base_point, summation_image

    return base_point, None


def stack_images(scale, images_array):
    rows = len(images_array)
    cols = len(images_array[0])

    available_rows = isinstance(images_array[0], list)
    width = images_array[0][0].shape[1]
    height = images_array[0][0].shape[0]

    if available_rows:
        for x in range(0, rows):
            for y in range(0, cols):
                if images_array[x][y].shape[:2] == images_array[0][0].shape[:2]:
                    images_array[x][y] = cv2.resize(
                        images_array[x][y], (0, 0), None, scale, scale
                    )
                else:
                    images_array[x][y] = cv2.resize(
                        images_array[x][y],
                        (images_array[0][0].shape[1], images_array[0][0].shape[0]),
                        None,
                        scale,
                        scale,
                    )

                if len(images_array[x][y].shape) == 2:
                    images_array[x][y] = cv2.cvtColor(
                        images_array[x][y], cv2.COLOR_GRAY2BGR
                    )

        blank_image = np.zeros((height, width, 3), np.uint8)
        hor = [blank_image] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(images_array[x])

        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if images_array[x].shape[:2] == images_array[0].shape[:2]:
                images_array[x] = cv2.resize(
                    images_array[x], (0, 0), None, scale, scale
                )
            else:
                images_array[x] = cv2.resize(
                    images_array[x],
                    (images_array[0].shape[1], images_array[0].shape[0]),
                    None,
                    scale,
                    scale,
                )

            if len(images_array[x].shape) == 2:
                images_array[x] = cv2.cvtColor(images_array[x], cv2.COLOR_GRAY2BGR)

        hor = np.hstack(images_array)
        ver = hor

    return ver
