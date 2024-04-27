import RPi.GPIO as GPIO
import time
import argparse


def pulse():
    step_pin = 27
    steps_per_second = 8000

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(step_pin, GPIO.OUT)

    pulse_frequency = int(steps_per_second)

    print(f"pulse_frequency: {pulse_frequency}")

    pwm = GPIO.PWM(step_pin, pulse_frequency)
    pwm.start(50)  # start PWM at 50% duty cycle

    time.sleep(20)

    # print(f"Acceleration steps: {acceleration_steps}")

    # for i in range(acceleration_steps):
    #     # pwm.ChangeFrequency(int(current_frequency))

    pwm.stop()  # Stop sending pulses

    GPIO.cleanup()


pulse()
