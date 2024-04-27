#!/usr/bin/env python

import time

import pigpio

start_frequency = 1
end_frequency = 10000
start_interval = 5000
end_interval = 100
STEP = 100

GPIO = 27

pi = pigpio.pi()

pi.set_mode(GPIO, pigpio.OUTPUT)

pi.wave_clear()


wf = []

for delay in range(start_interval, end_interval, -STEP):
    wf.append(pigpio.pulse(1 << GPIO, 0, delay))
    wf.append(pigpio.pulse(0, 1 << GPIO, delay))

pi.wave_add_generic(wf)

# add lots of pulses at final rate to give timing lee-way

wf = []

# add after existing pulses

offset = pi.wave_get_micros()

print("ramp is {} micros".format(offset))

wf.append(pigpio.pulse(0, 0, offset))

for i in range(2000):
    wf.append(pigpio.pulse(1 << GPIO, 0, end_interval))
    wf.append(pigpio.pulse(0, 1 << GPIO, end_interval))

pi.wave_add_generic(wf)

wid1 = pi.wave_create()

# send ramp, stop when final rate reached

pi.wave_send_once(wid1)

time.sleep(float(offset) / 1000000.0)  # make sure it's a float

pi.wave_send_repeat(wid0)

time.sleep(1)

pi.wave_tx_stop()

pi.stop()
