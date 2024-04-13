import pigpio
import time

# Constants
step_pin = 9  # GPIO pin for the STEP signal
dir_pin = 22  # GPIO pin for the DIRECTION signal
target_speed_rpm = 60
single_revolution_steps = 4000
steps_per_second = target_speed_rpm / 60 * single_revolution_steps

# Setup
pi = pigpio.pi()
if not pi.connected:
    exit()

# Set up GPIO pins
pi.set_mode(step_pin, pigpio.OUTPUT)
pi.set_mode(dir_pin, pigpio.OUTPUT)

# Set direction (1 for clockwise, 0 for counterclockwise)
pi.write(dir_pin, 1)

# Calculate pulse frequency based on desired speed
pulse_frequency = int(steps_per_second)

# Generate pulses
pi.set_PWM_frequency(step_pin, pulse_frequency)
pi.set_PWM_dutycycle(step_pin, 128)  # 50% duty cycle

# Run motor for 5 seconds
time.sleep(5)

# Stop motor
pi.set_PWM_dutycycle(step_pin, 0)  # Stop sending pulses

# Cleanup
pi.stop()
