import os
import shutil
from automatic_capture import capture_images_with_charuco
from camera_calibration import calibrate_and_save_parameters

# Define the directory for calibration images
calibration_images_dir = 'calibration_images'

# Remove the existing directory and all its contents
if os.path.exists(calibration_images_dir):
    shutil.rmtree(calibration_images_dir)

# Create a new directory for calibration images
os.mkdir(calibration_images_dir)

# Number of images to capture
NUM_IMAGES = 50

# Capture images with the Charuco board
capture_images_with_charuco(NUM_IMAGES)
calibrate_and_save_parameters(calibration_images_dir)
