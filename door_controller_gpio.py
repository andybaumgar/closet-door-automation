import RPi.GPIO as GPIO
import time
import argparse


def move(speed_rpm=60, direction=0, duration_seconds=2):
    # Constants
    step_pin = 9  # GPIO pin for the STEP signal
    dir_pin = 22  # GPIO pin for the DIRECTION signal
    single_revolution_steps = 4000
    steps_per_second = speed_rpm / 60 * single_revolution_steps

    # Setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(step_pin, GPIO.OUT)
    GPIO.setup(dir_pin, GPIO.OUT)

    GPIO.output(dir_pin, GPIO.HIGH if direction else GPIO.LOW)
    time.sleep(0.1)

    pulse_frequency = int(steps_per_second)
    pulse_width = 0.01  # seconds

    segment_duration = 0.1
    acceleration_duration = duration_seconds / 2
    acceleration_steps = int(acceleration_duration / segment_duration)
    pulse_frequency_increment = pulse_frequency / acceleration_steps
    current_frequency = 0

    # PWM Setup
    pwm = GPIO.PWM(step_pin, current_frequency)
    pwm.start(50)  # start PWM at 50% duty cycle

    print(f"Acceleration steps: {acceleration_steps}")

    for i in range(acceleration_steps):
        pwm.ChangeFrequency(int(current_frequency))
        current_frequency += pulse_frequency_increment
        time.sleep(segment_duration)

    for i in range(acceleration_steps):
        pwm.ChangeFrequency(int(current_frequency))
        current_frequency -= pulse_frequency_increment
        time.sleep(segment_duration)

    # Stop motor
    pwm.stop()  # Stop sending pulses

    # Cleanup
    GPIO.cleanup()


def main(args):
    move(
        speed_rpm=args.speed_rpm,
        direction=args.direction,
        duration_seconds=args.duration_seconds,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to move servo motor.")

    parser.add_argument("speed_rpm", type=float)
    parser.add_argument("direction", type=int)
    parser.add_argument("duration_seconds", type=float)

    args = parser.parse_args()

    main(args)
