import os
import numpy as np
import cv2

# Parameters
# -------------------
ARUCO_DICT = cv2.aruco.DICT_6X6_250
SQUARES_VERTICALLY = 7
SQUARES_HORIZONTALLY = 5
SQUARE_LENGTH = 0.03
MARKER_LENGTH = 0.015

# -------------------

# Function to calibrate and save parameters


def calibrate_and_save_parameters(PATH_TO_IMAGES='calibration_images'):
    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    board = cv2.aruco.CharucoBoard(
        (SQUARES_VERTICALLY, SQUARES_HORIZONTALLY), SQUARE_LENGTH, MARKER_LENGTH, dictionary)
    params = cv2.aruco.DetectorParameters()

    image_files = [os.path.join(PATH_TO_IMAGES, f) for f in os.listdir(
        PATH_TO_IMAGES) if f.endswith(".png")]
    image_files.sort()

    all_charuco_corners = []
    all_charuco_ids = []

    if not image_files:
        print("No images found")
        return

    for image_file in image_files:
        print(f"Processing {image_file}")
        image = cv2.imread(image_file)
        if image is None:
            print(f"Failed to read image {image_file}")
            continue

        marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(
            image, dictionary, parameters=params)
        if marker_ids is not None and len(marker_ids) > 0:
            charuco_retval, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(
                markerCorners=marker_corners, markerIds=marker_ids, image=image, board=board)
            if charuco_retval > 0 and len(charuco_corners) > 6:
                all_charuco_corners.append(charuco_corners)
                all_charuco_ids.append(charuco_ids)
            else:
                print(f"No Charuco corners detected in image {image_file}")
                os.remove(image_file)
        else:
            print(f"No markers detected in image {image_file}")
            os.remove(image_file)

    if not all_charuco_corners:
        print("No Charuco corners found in any images")
        return

    image_size = image.shape[:2]
    retval, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
        charucoCorners=all_charuco_corners, charucoIds=all_charuco_ids, board=board, imageSize=image_size, cameraMatrix=None, distCoeffs=None)

    np.save('camera_matrix.npy', camera_matrix)
    np.save('dist_coeffs.npy', dist_coeffs)

    # image_files = [os.path.join(PATH_TO_IMAGES, f) for f in os.listdir(
    #     PATH_TO_IMAGES) if f.endswith(".png")]
    # for image_file in image_files:
    #     image = cv2.imread(image_file)
    #     if image is None:
    #         print(f"Failed to read image {image_file}")
    #         continue
    #     undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs)
    #     cv2.imshow('Undistorted Image', undistorted_image)
    #     cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Calibration completed")


if __name__ == "__main__":
    calibrate_and_save_parameters()
