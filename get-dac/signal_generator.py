import numpy
import math
import time

def get_sin_wave_amplitude(freq,time,amplitude):
    res = 0.5*amplitude*(1-math.sin(float(2*math.pi*time*freq)))
    return res
def wait_for_sampling_period(sampling_frequency):
    time.sleep(1/sampling_frequency)