import r2r_adc
from time import time
import adc_plot


if __name__ == "__main__":
    dynamic_range = 3
    gpio_bits = [11,25,12,13,16,19,20,26]
    gpio_bits = gpio_bits[::-1]
    comp_pin = 21

    acd = r2r_adc.R2R_ADC(gpio_bits, dynamic_range, comp_pin, 0.0005, True)

    times = []
    mess = []
    experement_time = 5

    try:
        t0 = time()

        while(time() - t0 < experement_time):
            mes = acd.get_sar_voltage()
            t1 = time()
            times.append(t1-t0)
            mess.append(mes)
        if len(times) == 0:
            times = [0]
            mess = [0]
        adc_plot.plot_voltage_vs_time(times, mess)
        adc_plot.plot_sampling_period_hist(times)
    finally:
        acd.deinit()