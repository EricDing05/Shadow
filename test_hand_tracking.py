import cv2
import mediapipe as mp

# Initialize Mediapipe Hand Tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Start Webcam (Use 0 for default camera, change to 1 if using an external webcam)
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
                    print("🖐️ Fist Detected! 🛠️")
                else:
                    print("✋ Hand Open")

        # Display the camera feed
        cv2.imshow("Hand Tracking", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
