# %%
from __future__ import print_function
import sys
from pysmu import Mode, Session
import random
import time
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

if sys.stdout.isatty():
    output = lambda s: sys.stdout.write("\r" + s)
else:
    output = print

def refill_data(num_samples, v=None):
    if v is None:
        # fill channels with a static, random integer between 0 and 5
        v = random.randint(0, 5)
    return [v] * num_samples

n = 100000
# %%
session = Session()

if session.devices:
    # Grab the first device from the session.
    dev = session.devices[0]

    # Set both channels to source voltage, measure current mode.
    chan_a = dev.channels['A']
    chan_b = dev.channels['B']

    # %%
    chan_a.mode = Mode.SVMI
    chan_b.mode = Mode.SVMI
    #chan_a.mode = Mode.SIMV
    #chan_b.mode = Mode.SIMV

    i = 0
    num_samples = session.queue_size + 1
    start = time.time()

    while True:
        # Change written value approximately every second.
        if time.time() - start > 1:
            i += 1
            start = time.time()

        # Write iterating voltage values to both channels.
        chan_a.write(refill_data(num_samples, i % 6))
        chan_b.write(refill_data(num_samples, i % 6))

        # Read incoming samples in a blocking fashion.
        samples = dev.get_samples(num_samples)
        for x in samples:
            output("{: 6f} {: 6f} {: 6f} {: 6f}".format(x[0][0], x[0][1], x[1][0], x[1][1]))
else:
    print('no devices attached')
# %%
voltage_result = []
current_result = []
n = 50000
chan_a.flush()
for i in np.linspace(1, 5, 21):
    chan_a.write([i]*n)
    data = chan_a.get_samples(n)
    voltage = np.array(data)[:,0]
    current = np.array(data)[:,1]
    voltage_result.append(voltage.mean())
    current_result.append(current.mean())
voltage_result = np.array(voltage_result)
current_result = np.array(current_result)
plt.plot(voltage_result, voltage_result/current_result, 'x')

# %%
chan_a.flush()
chan_a.mode = Mode.SVMI
# Define the range and number of points
start = 0
peak = 5
num_points = 1000

# Create the rising and falling edges
rising = np.linspace(start, peak, num_points // 2)
falling = np.linspace(peak, start, num_points // 2)

# Concatenate to form the triangle wave
vals = np.concatenate((rising, falling))
chan_a.write(vals)
data = np.array(chan_a.get_samples(2000))
voltage = data[:,0]
current = data[:,1]
plt.plot(current)
# %%
# Test a sweep

n_s = 100
chan_a.flush()
chan_a.mode = Mode.SVMI
# Define the range and number of points
start = 0
peak = 5
num_points = 21
voltage_result = []
current_result = []
for voltage in np.linspace(0, 5, num_points):
    chan_a.write([voltage]*n_s)
    data = chan_a.get_samples(n_s)
    voltage = np.array(data)[:,0].mean()
    voltage_result.append(voltage)
    current = np.array(data)[:,1].mean()
    current_result.append(current)
plt.plot(voltage_result, current_result, 'x')


# %%
