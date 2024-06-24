import cv2

# Parameters
# -------------------
ARUCO_DICT = cv2.aruco.DICT_6X6_250
SQUARES_VERTICALLY = 7
SQUARES_HORIZONTALLY = 5
SQUARE_LENGTH = 0.03
MARKER_LENGTH = 0.02
LENGTH_PX = 900
MARGIN_PX = 30
SAVE_NAME = 'charuco.png'
# -------------------

# Function to create and save a Charuco board


def create_and_save_new_board():
    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    board = cv2.aruco.CharucoBoard(
        (SQUARES_VERTICALLY, SQUARES_HORIZONTALLY), SQUARE_LENGTH, MARKER_LENGTH, dictionary)
    size_ratio = SQUARES_HORIZONTALLY / SQUARES_VERTICALLY
    img = board.generateImage((LENGTH_PX, int(LENGTH_PX * size_ratio)),
                              marginSize=MARGIN_PX)
    while True:
        cv2.imshow('Press Enter to Capture Image, q to Quit', img)
        key = cv2.waitKey(1)
        if key == 13:  # 13 is the Enter key
            # Save the captured frame to an image file
            cv2.imwrite(SAVE_NAME, img)
            print("Image saved.")
            break
        elif key == ord('q'):  # 'q' key to quit
            print("Exiting...")
            break


if __name__ == "__main__":
    create_and_save_new_board()
