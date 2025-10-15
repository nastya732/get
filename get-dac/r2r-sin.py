import r2r_dac as r2r
import signal_generator as sg
import RPi.GPIO as GPIO
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

gpio_bits = [16, 20,21,25,26,17,27,22]

if __name__ == "__main__":
    try:
        dac = r2r.R2R_DAC(gpio_bits, amplitude, True)
        while True:
            sg.wait_for_sampling_period(sampling_frequency)
            voltage = sg.get_sin_wave_amplitude(signal_frequency,time.time())
            GPIO.output(gpio_bits, dac.number_to_dac(abs(int(voltage*255))))
    finally:
        dac.deinit()