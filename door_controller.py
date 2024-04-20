import pigpio
import time
import argparse


def move(speed_rpm=60, direction=0, duration_seconds=2):
    # Constants
    step_pin = 9  # GPIO pin for the STEP signal
    dir_pin = 22  # GPIO pin for the DIRECTION signal
    single_revolution_steps = 4000
    steps_per_second = speed_rpm / 60 * single_revolution_steps

    # Setup
    pi = pigpio.pi()
    if not pi.connected:
        exit()

    # Set up GPIO pins
    pi.set_mode(step_pin, pigpio.OUTPUT)
    pi.set_mode(dir_pin, pigpio.OUTPUT)

    # Set direction (1 for clockwise, 0 for counterclockwise)
    pi.write(dir_pin, direction)
    time.sleep(0.1)

    # Calculate pulse frequency based on desired speed
    pulse_frequency = int(steps_per_second)

    # Generate pulses
    pi.set_PWM_frequency(step_pin, pulse_frequency)
    pi.set_PWM_dutycycle(step_pin, 128)  # 50% duty cycle

    # Run motor for 5 seconds
    time.sleep(duration_seconds)

    # Stop motor
    pi.set_PWM_dutycycle(step_pin, 0)  # Stop sending pulses

    # Cleanup
    pi.stop()


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
