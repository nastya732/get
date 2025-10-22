import time
from r2r_adc import R2R_ADC
from adc_plot import plot_voltage_vs_time

def main():
    adc = R2R_ADC(dynamic_range=3.3, verbose=False)
    voltage_values = []
    time_values = []
    duration = 3.0
    
    try:
        start_time = time.time()
        print(f"Измеряю напряжение {duration} секунд...")
        print("Крутите потенциометр во время измерений!")
        
        while (time.time() - start_time) < duration:
            current_voltage = adc.get_sc_voltage()
            current_time = time.time() - start_time
            
            voltage_values.append(current_voltage)
            time_values.append(current_time)
            
            print(f"Время: {current_time:.1f}с, Напряжение: {current_voltage:.2f}В")
            time.sleep(0.1)
        
        print("Измерения завершены! Строю график...")
        
        # Построение графика
        plot_voltage_vs_time(time_values, voltage_values, adc.dynamic_range)
        
        print("Если не видите график, проверьте файл 'voltage_plot.png' в папке!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        adc.__del__()

if __name__ == "__main__":
    main()