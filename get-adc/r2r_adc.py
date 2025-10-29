# r2r_adc.py
import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)
    
    def __del__(self):
        """Деструктор - выставляет 0 на ЦАП и очищает GPIO"""
        for pin in self.bits_gpio:
            GPIO.output(pin, 0)
        GPIO.cleanup()
        if self.verbose:
            print("R2R_ADC: ЦАП обнулен, GPIO очищен")
    
    def number_to_dac(self, number):
        """Подает число number на вход ЦАП и возвращает битовое представление"""
        if number < 0 or number >= 2**len(self.bits_gpio):
            raise ValueError(f"Число {number} вне диапазона 0-{2**len(self.bits_gpio)-1}")
        
        bits = [int(element) for element in bin(number)[2:].zfill(8)]
        
        for i, pin in enumerate(self.bits_gpio):
            GPIO.output(pin, bits[i])
        
        if self.verbose:
            print(f"R2R_ADC: Подано число {number} (бинарно: {''.join(map(str, bits))}) на ЦАП")
        
        return bits
    
    def sequential_counting_adc(self):
        """Последовательный подсчет АЦП"""
        max_value = 2**len(self.bits_gpio) - 1
        
        for number in range(max_value + 1):
            self.number_to_dac(number)
            time.sleep(self.compare_time)
            comparator_output = GPIO.input(self.comp_gpio)
            
            if self.verbose:
                print(f"Число: {number}, Компаратор: {comparator_output}")
            
            if comparator_output == 1:
                if self.verbose:
                    print(f"Напряжение превышено при числе: {number}")
                return number
        
        if self.verbose:
            print(f"Достигнут максимум: {max_value}")
        return max_value
    
    def get_sc_voltage(self):
        """Возвращает измеренное напряжение в Вольтах (последовательный подсчет)"""
        digital_value = self.sequential_counting_adc()
        max_digital = 2**len(self.bits_gpio) - 1
        voltage = (digital_value / max_digital) * self.dynamic_range
        
        if self.verbose:
            print(f"Цифровое значение: {digital_value}, Напряжение: {voltage:.3f} В")
        
        return voltage

    def successive_approximation_adc(self):
        """Алгоритм бинарного поиска напряжения на входе АЦП"""
        max_value = 2**len(self.bits_gpio) - 1
        result = 0
        
        # Проходим по всем битам, начиная со старшего
        for bit in range(len(self.bits_gpio) - 1, -1, -1):
            # Устанавливаем текущий бит в 1
            current_value = result | (1 << bit)
            
            # Подаем значение на ЦАП
            self.number_to_dac(current_value)
            time.sleep(self.compare_time)
            
            # Читаем компаратор
            comparator_output = GPIO.input(self.comp_gpio)
            
            if self.verbose:
                print(f"Бит {bit}: значение {current_value}, компаратор: {comparator_output}")
            
            # Если напряжение ЦАП <= входного напряжения (компаратор = 0)
            # Оставляем бит установленным
            if comparator_output == 0:
                result = current_value
            # Иначе (компаратор = 1) - напряжение ЦАП > входного напряжения
            # Сбрасываем текущий бит
            else:
                result = result & ~(1 << bit)
        
        if self.verbose:
            print(f"Найдено значение: {result}")
        
        return result
    
    def get_sar_voltage(self):
        """Возвращает измеренное алгоритмом бинарного поиска напряжение в Вольтах"""
        digital_value = self.successive_approximation_adc()
        max_digital = 2**len(self.bits_gpio) - 1
        voltage = (digital_value / max_digital) * self.dynamic_range
        
        if self.verbose:
            print(f"SAR - Цифровое значение: {digital_value}, Напряжение: {voltage:.3f} В")
        
        return voltage


# Основной охранник для SAR АЦП
if __name__ == "__main__":
    try:
        # Создаем объект АЦП (dynamic_range замените на измеренное значение!)
        adc = R2R_ADC(dynamic_range=3.3, verbose=True)
        
        print("SAR АЦП запущен! Крутите потенциометр и наблюдайте изменение напряжения.")
        print("Нажмите Ctrl+C для остановки.")
        print("-" * 50)
        
        # Бесконечный цикл измерений
        while True:
            # Читаем напряжение методом get_sar_voltage()
            voltage = adc.get_sar_voltage()
            
            # Печатаем в терминал
            print(f"SAR Напряжение: {voltage:.3f} В", end='\r')
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\nИзмерения остановлены пользователем")
    finally:
        # Вызываем деструктор
        if 'adc' in locals():
            adc.__del__()
        print("GPIO очищен, программа завершена.")