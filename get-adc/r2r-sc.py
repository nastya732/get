# r2r-sc.py
import time
from r2r_adc import R2R_ADC  # Предполагается, что ваш класс в файле r2r_adc.py
from adc_plot import plot_voltage_vs_time

def main():
    # Создаем объект класса R2R_ADC
    adc = R2R_ADC(dynamic_range=1.357, verbose=False) 
    
    # Списки для хранения данных
    voltage_values = []
    time_values = []
    duration = 3.0  # Продолжительность измерений в секундах
    
    try:
        # Сохраняем момент начала эксперимента
        start_time = time.time()
        
        print(f"Начало измерений на {duration} секунд...")
        
        # Пока разница между текущим временем и начальным меньше продолжительности
        while (time.time() - start_time) < duration:
            # Измеряем напряжение
            current_voltage = adc.get_sc_voltage()
            current_time = time.time() - start_time
            
            # Добавляем в списки
            voltage_values.append(current_voltage)
            time_values.append(current_time)
            
            # Выводим прогресс (опционально)
            print(f"Время: {current_time:.2f} с, Напряжение: {current_voltage:.3f} В")
            
            # Небольшая пауза между измерениями
            time.sleep(0.1)
        
        print("Измерения завершены. Построение графика...")
        
        # Отображаем график
        plot_voltage_vs_time(time_values, voltage_values, adc.dynamic_range)
    
    finally:
        # Вызываем деструктор
        adc.__del__()
        print("Программа завершена, GPIO очищен")
