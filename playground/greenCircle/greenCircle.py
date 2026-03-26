import cv2
import numpy as np

def check_for_green_circles():
    cap = cv2.VideoCapture(0)

    # Open a new window for the cam feed (original frame)
    cv2.namedWindow('Camera Feed', cv2.WINDOW_NORMAL)
    # Open a window for the green circles detection output
    cv2.namedWindow('Green Circles Detection', cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("not ret :(((())))")
            break

        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define range for green color in HSV
        lower_green = np.array([40, 70, 70])
        upper_green = np.array([80, 255, 255])

        # Create a mask for green color
        mask = cv2.inRange(hsv, lower_green, upper_green)
        output = cv2.bitwise_and(frame, frame, mask=mask)

        # Convert mask to grayscale for circle detection
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

        # Use HoughCircles to detect circles
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1.5,
            minDist=50,
            param1=45,
            param2=30,
            minRadius=10,
            maxRadius=100
        )
        
        # Draw detected circles
        detected_frame = frame.copy()
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                cv2.circle(detected_frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                cv2.circle(detected_frame, (i[0], i[1]), 2, (0, 0, 255), 3)

        # Show the original frame in one window
        cv2.imshow('Camera Feed', frame)
        # Show the detected circles in the other window
        cv2.imshow('Green Circles Detection', detected_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


check_for_green_circles()
print("success :)")