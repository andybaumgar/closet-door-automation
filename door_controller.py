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

    pi.set_mode(step_pin, pigpio.OUTPUT)
    pi.set_mode(dir_pin, pigpio.OUTPUT)

    pi.write(dir_pin, direction)
    time.sleep(0.1)

    pulse_frequency = int(steps_per_second)

    segment_duration = 0.05
    acceleration_duration = duration_seconds / 2
    acceleration_steps = acceleration_duration / segment_duration
    pulse_frequency_increment = pulse_frequency / acceleration_steps
    current_frequency = 0

    print(f"Acceleration steps: {acceleration_steps}")

    for i in range(int(acceleration_steps)):
        pi.set_PWM_frequency(step_pin, int(current_frequency))
        pi.set_PWM_dutycycle(step_pin, 128)
        current_frequency += pulse_frequency_increment
        print(f"Frequency: {current_frequency}")
        time.sleep(segment_duration)  # 50% duty cycle

    for i in range(int(acceleration_steps)):
        pi.set_PWM_frequency(step_pin, int(current_frequency))
        pi.set_PWM_dutycycle(step_pin, 128)
        current_frequency -= pulse_frequency_increment
        print(f"Frequency: {current_frequency}")
        time.sleep(segment_duration)  # 50% duty cycle

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
