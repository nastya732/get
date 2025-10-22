import pwm_dac
import signal_generator as sg
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000
gpio_pin = 12

if __name__ == "__main__":
    try:
        dac = pwm_dac.PWM_DAC(gpio_pin, sampling_frequency, amplitude, True)
        while True:
            sg.wait_for_sampling_period(sampling_frequency)
            voltage = sg.get_sin_wave_amplitude(signal_frequency,time.time())
            dac.set_voltage(voltage*amplitude)
    finally:
        dac.deinit()