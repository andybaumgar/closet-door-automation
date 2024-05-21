import RPi.GPIO as GPIO
import time

SPEED_RPM = 60
CLOCKWISE_DIRECTION = False
DURATION_SECONDS = 2

BUTTON_PIN = 17  # set button pin


def move(speed_rpm=60, clockwise_direction=False, duration_seconds=2):
    step_pin = 13  # GPIO pin for the STEP signal
    dir_pin = 5  # GPIO pin for the DIRECTION signal
    single_revolution_steps = 100
    steps_per_second = speed_rpm / 60 * single_revolution_steps

    # Setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(step_pin, GPIO.OUT)
    GPIO.setup(dir_pin, GPIO.OUT)

    GPIO.output(dir_pin, GPIO.HIGH if clockwise_direction else GPIO.LOW)
    time.sleep(0.1)

    pulse_frequency = int(steps_per_second)

    segment_duration = 0.1
    acceleration_duration = duration_seconds / 2
    acceleration_steps = int(acceleration_duration / segment_duration)
    pulse_frequency_increment = pulse_frequency / acceleration_steps
    current_frequency = 1

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


def setup():
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def button_clicked():
    return GPIO.input(BUTTON_PIN)


def print_door_status(door_closed):
    print("Door closed" if door_closed else "Door opened")


def run_door():
    setup()

    door_closed = True
    print_door_status(door_closed)

    current_direction = CLOCKWISE_DIRECTION

    if button_clicked():
        print("Button pressed while starting. Please check the wiring.  Exiting.")
        return

    while True:
        if button_clicked():
            move(
                speed_rpm=SPEED_RPM,
                clockwise_direction=current_direction,
                duration_seconds=DURATION_SECONDS,
            )

            door_closed = not door_closed
            print_door_status(door_closed)

            current_direction = not current_direction


run_door()
