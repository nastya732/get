# # r2r-sc.py
# import time
# from r2r_adc import R2R_ADC
# from adc_plot import plot_voltage_vs_time, plot_sampling_period_hist

# def main():
#     adc = R2R_ADC(dynamic_range=3.3, verbose=False)
#     voltage_values = []
#     time_values = []
#     duration = 10.0
#     measure_interval = 0.02
    
#     try:
#         start_time = time.time()
#         print(f"Измеряю {duration} секунд с интервалом {measure_interval}с")
#         print("Крутите потенциометр во время измерений!")
        
#         while (time.time() - start_time) < duration:
#             current_voltage = adc.get_sc_voltage()
#             current_time = time.time() - start_time
            
#             voltage_values.append(current_voltage)
#             time_values.append(current_time)
            
#             # Реже выводим в консоль чтобы не засорять
#             if len(voltage_values) % 10 == 0:
#                 print(f"Измерено точек: {len(voltage_values)}")
            
#             time.sleep(measure_interval)
        
#         print(f"Измерения завершены! Всего точек: {len(voltage_values)}")
        
#         # Отображение графика напряжения
#         plot_voltage_vs_time(time_values, voltage_values, adc.dynamic_range)
        
#         # Отображение гистограммы периодов измерений
#         plot_sampling_period_hist(time_values)
        
#     except Exception as e:
#         print(f"Ошибка: {e}")
#     finally:
#         adc.__del__()

# if __name__ == "__main__":
#     main()
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
            mes = acd.get_sc_voltage()
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