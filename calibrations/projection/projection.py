import numpy as np
from projection_calibration_image import create_and_save_calibration_image
from projection_calibration import calibrate_projector

image_path = 'calibration_image.png'
camera_matrix = np.load('camera_matrix.npy')
dist_coeffs = np.load('dist_coeffs.npy')
width = 1920
height = 1080

create_and_save_calibration_image(image_path,
                                  camera_matrix, dist_coeffs, width, height)
calibrate_projector(image_path, width, height)
