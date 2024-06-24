import cv2
import numpy as np
import mediapipe as mp

# Initialize mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.1, min_tracking_confidence=0.1)

mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Load the transformation matrix, camera matrix, and distortion coefficients
M = np.load('M.npy')
camera_matrix = np.load('camera_matrix.npy')
dist_coeffs = np.load('dist_coeffs.npy')

width = 1920
height = 1080

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture image")
        break

    # Undistort the frame with the camera calibration
    frame = cv2.undistort(frame, camera_matrix, dist_coeffs)

    # Apply the perspective transformation
    warped_image = cv2.warpPerspective(frame, M, (width, height))

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(warped_image, cv2.COLOR_BGR2RGB)

    # Run inference for hands
    results = hands.process(rgb_frame)

    # Create a black image for drawing
    drawing_image = np.zeros((height, width, 3), np.uint8)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                drawing_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Rotate the image 180 degrees
    drawing_image = cv2.rotate(drawing_image, cv2.ROTATE_180)

    # Display the final image in fullscreen
    cv2.namedWindow("Final Image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(
        "Final Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Final Image", drawing_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
