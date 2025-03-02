import smbus
import time
import math
import RPi.GPIO as GPIO

# MPU6050 Registers & Address
MPU6050_ADDR_1 = 0x68  # IMU 1 (Upper Arm)
MPU6050_ADDR_2 = 0x69  # IMU 2 (Forearm)
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# Initialize I2C Bus
bus = smbus.SMBus(1)

# Wake up both IMUs
bus.write_byte_data(MPU6050_ADDR_1, PWR_MGMT_1, 0)
bus.write_byte_data(MPU6050_ADDR_2, PWR_MGMT_1, 0)

# Servo Setup (Raspberry Pi GPIO Pins)
SHOULDER_PITCH_PIN = 17
SHOULDER_ROLL_PIN = 18
ELBOW_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(SHOULDER_PITCH_PIN, GPIO.OUT)
GPIO.setup(SHOULDER_ROLL_PIN, GPIO.OUT)
GPIO.setup(ELBOW_PIN, GPIO.OUT)

shoulder_pitch_servo = GPIO.PWM(SHOULDER_PITCH_PIN, 50)
shoulder_roll_servo = GPIO.PWM(SHOULDER_ROLL_PIN, 50)
elbow_servo = GPIO.PWM(ELBOW_PIN, 50)

shoulder_pitch_servo.start(7.5)  # Neutral position
shoulder_roll_servo.start(7.5)
elbow_servo.start(7.5)

# Read data from MPU6050
def read_word(addr, register):
    high = bus.read_byte_data(addr, register)
    low = bus.read_byte_data(addr, register + 1)
    value = (high << 8) + low
    if value >= 0x8000:
        value = -((65535 - value) + 1)
    return value

# Get angles from an IMU
def get_angles(addr):
    accel_x = read_word(addr, ACCEL_XOUT_H)
    accel_y = read_word(addr, ACCEL_XOUT_H + 2)
    accel_z = read_word(addr, ACCEL_XOUT_H + 4)

    # Convert acceleration to angles
    angle_x = math.atan2(accel_y, accel_z) * (180 / math.pi)  # Pitch
    angle_y = math.atan2(accel_x, accel_z) * (180 / math.pi)  # Roll

    return angle_x, angle_y

# Move servo function
def move_servo(servo, angle):
    duty = (angle / 18) + 2  # Convert angle to PWM duty cycle
    servo.ChangeDutyCycle(duty)
    time.sleep(0.05)

# Main loop: Read IMU data & move robotic arm
try:
    while True:
        # Read angles from both IMUs
        shoulder_pitch, shoulder_roll = get_angles(MPU6050_ADDR_1)
        forearm_pitch, _ = get_angles(MPU6050_ADDR_2)  # Only need forearm pitch
        
        # Compute elbow bend angle (difference between upper arm and forearm angles)
        elbow_angle = forearm_pitch - shoulder_pitch
        
        # Map IMU angles to servo motors
        move_servo(shoulder_pitch_servo, shoulder_pitch)  # Move shoulder pitch
        move_servo(shoulder_roll_servo, shoulder_roll)  # Move shoulder roll
        move_servo(elbow_servo, elbow_angle)  # Move elbow

        time.sleep(0.1)  # Small delay

except KeyboardInterrupt:
    # Stop servos & cleanup
    shoulder_pitch_servo.stop()
    shoulder_roll_servo.stop()
    elbow_servo.stop()
    GPIO.cleanup()
    print("\nStopped and cleaned up.")
