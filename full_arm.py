import threading
import subprocess

# Run Hand Tracking in a Separate Thread
def run_hand_tracking():
    subprocess.run(["python3", "hand_tracking.py"])

# Run IMU-Based Arm Mirroring in Another Thread
def run_arm_mirroring():
    subprocess.run(["python3", "arm_mirroring.py"])

# Create Two Threads
hand_tracking_thread = threading.Thread(target=run_hand_tracking)
arm_mirroring_thread = threading.Thread(target=run_arm_mirroring)

# Start Both Threads
hand_tracking_thread.start()
arm_mirroring_thread.start()

# Wait for Both to Finish
hand_tracking_thread.join()
arm_mirroring_thread.join()
