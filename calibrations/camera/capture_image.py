import cv2
from uuid import uuid4


def capture_image():
    # Connect to the camera (0 is usually the default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    # Set the width and height of the frame
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        # Capture a single frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the captured frame
        cv2.imshow('Press Enter to Capture Image, q to Quit', frame)

        # Wait for key press
        key = cv2.waitKey(1)
        if key == 13:  # 13 is the Enter key
            # Save the captured frame to an image file
            filename = f'calibration_images/captured_image_{uuid4()}.png'
            cv2.imwrite(filename, frame)
            print(f"Image captured and saved as {filename}.")
        elif key == ord('q'):  # 'q' key to quit
            print("Exiting...")
            break

    # Release the camera and close the display window
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_image()
