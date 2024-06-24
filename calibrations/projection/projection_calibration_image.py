import cv2
import numpy as np
import time


def create_and_save_calibration_image(saving_path, camera_matrix, dist_coeffs, width, height):
    cap = cv2.VideoCapture(0)

    calibration_image = np.zeros((height, width, 3), np.uint8)
    calibration_image = cv2.rectangle(
        calibration_image, (20, 20), (width-20, height-20), (0, 255, 0), 20)

    # cv2.imshow('Calibration Image', calibration_image)
    # cv2.waitKey(0)

    # Diplay full image screen on the monitor
    cv2.namedWindow('Calibration frame', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Calibration frame',
                          cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Calibration frame', calibration_image)
    cv2.waitKey(0)
    time.sleep(1)
    sucess, image = cap.read()

    # cv2.imshow('Captured image', image)
    # cv2.waitKey(0)

    cv2.imwrite(saving_path, image)


if __name__ == "__main__":
    saving_path = 'calibration_image.png'
    camera_matrix = np.load('camera_matrix.npy')
    dist_coeffs = np.load('dist_coeffs.npy')
    width = 1920
    height = 1080

    create_and_save_calibration_image(saving_path,
                                      camera_matrix, dist_coeffs, width, height)
    cv2.destroyAllWindows()
