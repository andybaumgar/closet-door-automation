import time
import argparse
import pigpio


def pulse():

    pi = pigpio.pi()
    if not pi.connected:
        exit()

    k_steps_per_second = input("Enter frequency in KHz: ")

    step_pin = 27
    steps_per_second = int(k_steps_per_second) * 1000
    pulse_frequency = int(steps_per_second)

    pi.set_mode(step_pin, pigpio.OUTPUT)

    pi.set_PWM_dutycycle(step_pin, 128)

    pi.set_PWM_frequency(step_pin, pulse_frequency)

    time.sleep(10)

    pi.set_PWM_dutycycle(step_pin, 0)  # Stop sending pulses
    pi.stop()


pulse()
