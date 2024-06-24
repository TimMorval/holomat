import cv2
import numpy as np

width = 1920
height = 1080


def calibrate_projector(image_path, width, height):
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold_value = 40

    _, thresholded_image = cv2.threshold(
        gray, threshold_value, 255, cv2.THRESH_BINARY)

    thresholded_image = thresholded_image.astype('uint8')

    # Find contours
    contours, _ = cv2.findContours(
        thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out only closed contours
    closed_contours = []
    for contour in contours:
        # Filter out small areas for noise reduction
        if cv2.contourArea(contour) > 100:
            if cv2.isContourConvex(contour) or len(contour) >= 4:
                closed_contours.append(contour)

    if not closed_contours:
        print("No closed contours found")
        exit()

    # Find the largest closed contour
    largest_contour = max(closed_contours, key=cv2.contourArea)

    # Draw the largest closed contour
    cv2.drawContours(image, [largest_contour], -1, (0, 0, 255), 2)

    # Approximate the largest contour with a polygon
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    projection_approx_corners = cv2.approxPolyDP(
        largest_contour, epsilon, True)

    if len(projection_approx_corners) == 4:
        for i, corner in enumerate(projection_approx_corners):
            x, y = corner.ravel()
            print(f"Corner {i+1}: ({x}, {y})")
            cv2.circle(image, (x, y), 5, (0, 0, 255), -1)
    else:
        print("Could not find the projection corners")

    cv2.imshow('Projection Corners', image)
    cv2.waitKey(0)

    if len(projection_approx_corners) == 4:
        points = projection_approx_corners.reshape(4, 2).astype('float32')

        # Calculate the sum and difference of the points
        s = points.sum(axis=1)
        diff = np.diff(points, axis=1)

        # Order the points: top-left, top-right, bottom-right, bottom-left
        ordered_points = np.zeros((4, 2), dtype="float32")
        ordered_points[0] = points[np.argmin(s)]  # top-left
        ordered_points[2] = points[np.argmax(s)]  # bottom-right
        ordered_points[1] = points[np.argmin(diff)]  # top-right
        ordered_points[3] = points[np.argmax(diff)]  # bottom-left

        for i, corner in enumerate(ordered_points):
            x, y = corner.ravel()
            print(f"Ordered corner {i+1}: ({x}, {y})")

        dst_points = np.array(
            [[0, 0], [width-1, 0], [width-1, height-1], [0, height-1]], dtype='float32')

        M = cv2.getPerspectiveTransform(ordered_points, dst_points)
        warped_image = cv2.warpPerspective(image, M, (width, height))

        cv2.imshow('Warped Image', warped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Could not find 4 corners for the transformation")

    np.save('M.npy', M)
    print("Projection calibration completed")


if __name__ == "__main__":
    calibrate_projector('calibration_image.png', width, height)
