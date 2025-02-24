# Shadow
# Shadow's Software

# libraries
import RPi.GPIO as GPIO
import time

# setup 
servo_pin = 7 # random pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Set up PWM (Pulse Width Modulation) at 50Hz (standard for servo motors)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)  # Start PWM with 0 duty cycle (no movement)

def move_servo(angle):
# Convert angle to duty cycle (corresponding PWM signal)
    duty = (angle / 18) + 2  # Formula for converting angle to PWM duty cycle (range 2-12)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)  # Wait for the servo to move to the position

try: 
# example to move servo to 0,90, and 180 degrees
    move.servo(0)
    time.sleep(1)
    move.servo(90)
    time.sleep(1)
    move.servo(180)
    time.sleep(1)

finally: 
    pwm.stop()
    GPIO.cleanup()