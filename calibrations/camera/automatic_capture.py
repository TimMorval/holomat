import cv2
from uuid import uuid4
import random
import os

# Load Charuco board image
charuco_img = cv2.imread('charuco.png')

if charuco_img is None:
    print("Error: Could not load Charuco board image.")
    exit()


def capture_images_with_charuco(n):
    # Connect to the camera (0 is usually the default camera)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    # Set the width and height of the frame
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 900)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 642)

    screen_width = 1920  # Adjust based on your screen resolution
    screen_height = 1080  # Adjust based on your screen resolution
    window_width = charuco_img.shape[1]
    window_height = charuco_img.shape[0]

    if not os.path.exists('calibration_images'):
        os.makedirs('calibration_images')

    for i in range(n):
        # Randomly position the Charuco board window on the screen
        x_pos = random.randint(0, screen_width - window_width)
        y_pos = random.randint(0, screen_height - window_height)

        # Display the Charuco board window at the random position
        cv2.namedWindow('Charuco Board', cv2.WINDOW_NORMAL)
        cv2.moveWindow('Charuco Board', x_pos, y_pos)
        cv2.imshow('Charuco Board', charuco_img)

        # Wait for a short period to allow for the window to be displayed
        cv2.waitKey(500)

        # Capture a single frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        # Save the captured frame to an image file
        filename = f'calibration_images/captured_image_{uuid4()}.png'
        cv2.imwrite(filename, frame)
        print(f"Image {i+1}/{n} captured and saved as {filename}.")

        # Close the Charuco board window
        cv2.destroyWindow('Charuco Board')

    # Release the camera and close the display window
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    num_images_to_capture = 100  # Set the number of images you want to capture
    capture_images_with_charuco(num_images_to_capture)
