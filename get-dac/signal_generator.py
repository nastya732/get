import numpy
import math
import time

def get_sin_wave_amplitude(freq,time):
    res = 0.5*(1-math.sin(float(2*3.14*time*freq)))
    return res
def wait_for_sampling_period(sampling_frequency):
    time.sleep(1/sampling_frequency)