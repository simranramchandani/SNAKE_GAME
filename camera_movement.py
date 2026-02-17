# camera_movement.py
# ------------------------------------------------------------
# This script uses OpenCV to detect a green object in front of
# the webcam and convert its position into directional commands.
# It divides the screen into zones (left/right/up/down) and
# outputs a direction when the object leaves the central "dead zone".
# ------------------------------------------------------------

import cv2
import numpy as np
import time

# HSV color range for detecting green objects
# These values can be adjusted depending on lighting conditions
GREEN_LOWER = (29, 86, 6)
GREEN_UPPER = (64, 255, 255)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Variables for debouncing direction changes
last_dir = None       # Last direction detected
last_time = 0         # Timestamp of last update
DEBOUNCE = 0.3        # Minimum time between direction updates (seconds)


def get_direction():
    """
    Reads a frame from the webcam, detects a green object,
    determines its position relative to the screen, and returns
    a direction ("left", "right", "up", "down") if movement is detected.

    Returns:
        str or None: The detected direction, or None if no update.
    """
    global last_dir, last_time

    # Read a frame from the camera
    ok, frame = cap.read()
    if not ok:
        return None

    # Resize for faster processing and flip for natural movement
    frame = cv2.resize(frame, (320, 240))
    frame = cv2.flip(frame, 1)

    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask that isolates green pixels
    mask = cv2.inRange(hsv, np.array(GREEN_LOWER), np.array(GREEN_UPPER))

    # Reduce noise in the mask
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)

    # Find contours (blobs) in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    h, w = frame.shape[:2]
    new_dir = None  # Direction detected this frame

    if contours:
        # Select the largest green contour
        cnt = max(contours, key=cv2.contourArea)

        # Ignore tiny noise blobs
        if cv2.contourArea(cnt) > 300:
            # Bounding box around the detected object
            x, y, cw, ch = cv2.boundingRect(cnt)
            cx, cy = x + cw // 2, y + ch // 2  # Center point of the object

            # Draw bounding box and center point for visual feedback
            cv2.rectangle(frame, (x, y), (x + cw, y + ch), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Define the "dead zone" in the center of the screen
            margin_x, margin_y = w // 4, h // 4
            left_band, right_band = margin_x, w - margin_x
            top_band, bottom_band = margin_y, h - margin_y

            # Draw dead zone rectangle
            cv2.rectangle(frame, (left_band, top_band), (right_band, bottom_band),(255, 200, 0), 1)

            # Determine direction only if object is outside the dead zone
            if cx < left_band:
                new_dir = "left"
            elif cx > right_band:
                new_dir = "right"
            elif cy < top_band:
                new_dir = "up"
            elif cy > bottom_band:
                new_dir = "down"

    # Debounce logic: update direction only if enough time has passed
    #this is were the import time is used
    now = time.time()
    if new_dir and (now - last_time) > DEBOUNCE:
        last_dir = new_dir
        last_time = now

    # Display the detected direction on the frame
    cv2.putText(frame, f"Direction: {last_dir}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Show the camera feed
    cv2.imshow("Gesture Control", frame)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        return None

    return last_dir


# ------------------------------------------------------------
# Standalone test mode: run this file directly to see the
# gesture detection in action and print directions to console.
# ------------------------------------------------------------
if __name__ == "__main__":
    while True:
        direction = get_direction()
        if direction:
            print("Detected:", direction)

        # Stop if the window is closed manually
        if cv2.getWindowProperty("Gesture Control", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()