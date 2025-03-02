import cv2
import mediapipe as mp
import RPi.GPIO as GPIO
import time

# GPIO Setup for Electromagnet (Using Pin 23)
ELECTROMAGNET_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(ELECTROMAGNET_PIN, GPIO.OUT)

# Initialize Mediapipe Hand Tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Start Raspberry Pi Camera
cap = cv2.VideoCapture(0)

def is_fist_closed(hand_landmarks):
    """
    Determines if the hand is in a 'fist' position by checking finger positions.
    Returns True if fist is closed, False otherwise.
    """
    finger_tips = [8, 12, 16, 20]  # Tip landmarks for index, middle, ring, and pinky fingers
    finger_mcp = [5, 9, 13, 17]    # MCP (knuckle) landmarks for those fingers

    closed_fingers = 0

    for tip, mcp in zip(finger_tips, finger_mcp):
        if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[mcp].y:  # If tip is below knuckle (closed)
            closed_fingers += 1

    return closed_fingers >= 3  # Consider it a fist if 3+ fingers are closed

try:
    while True:
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)  # Flip horizontally for mirror effect
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if is_fist_closed(hand_landmarks):
                    print("Fist Detected! Turning ON Electromagnet")
                    GPIO.output(ELECTROMAGNET_PIN, GPIO.HIGH)  # Turn ON electromagnet
                else:
                    print("Hand Open. Turning OFF Electromagnet")
                    GPIO.output(ELECTROMAGNET_PIN, GPIO.LOW)  # Turn OFF electromagnet

        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
