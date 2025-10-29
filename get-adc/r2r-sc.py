# r2r-sc.py
import time
from r2r_adc import R2R_ADC
from adc_plot import plot_voltage_vs_time, plot_sampling_period_hist

def main():
    adc = R2R_ADC(dynamic_range=3.3, verbose=False)
    voltage_values = []
    time_values = []
    duration = 10.0
    measure_interval = 0.02
    
    try:
        start_time = time.time()
        print(f"Измеряю {duration} секунд с интервалом {measure_interval}с")
        print("Крутите потенциометр во время измерений!")
        
        while (time.time() - start_time) < duration:
            current_voltage = adc.get_sc_voltage()
            current_time = time.time() - start_time
            
            voltage_values.append(current_voltage)
            time_values.append(current_time)
            
            # Реже выводим в консоль чтобы не засорять
            if len(voltage_values) % 10 == 0:
                print(f"Измерено точек: {len(voltage_values)}")
            
            time.sleep(measure_interval)
        
        print(f"Измерения завершены! Всего точек: {len(voltage_values)}")
        
        # Отображение графика напряжения
        plot_voltage_vs_time(time_values, voltage_values, adc.dynamic_range)
        
        # Отображение гистограммы периодов измерений
        plot_sampling_period_hist(time_values)
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        adc.__del__()

if __name__ == "__main__":
    main()