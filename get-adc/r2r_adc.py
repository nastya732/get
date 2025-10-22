import RPi.GPIO as GPIO
import time

# # Временный скрипт для измерения
# import RPi.GPIO as GPIO
# import time

# # Настройка GPIO как в вашем классе
# bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(bits_gpio, GPIO.OUT)

# # Подаем все единицы (255 для 8 бит) - максимальное напряжение
# binary_255 = [1,1,1,1,1,1,1,1]
# for i, pin in enumerate(bits_gpio):
#     GPIO.output(pin, binary_255[i])

# print("Подано 255 на ЦАП. Измерьте напряжение мультиметром!")

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
        max_value = 2**len(self.bits_gpio) - 1  # 255 для 8 бит
        
        for number in range(max_value + 1):
            # Подаем число на ЦАП
            self.number_to_dac(number)
            
            # Пауза для стабилизации компаратора
            time.sleep(self.compare_time)
            
            # Читаем состояние компаратора
            comparator_output = GPIO.input(self.comp_gpio)
            
            if self.verbose:
                print(f"Число: {number}, Компаратор: {comparator_output}")
            
            # Если напряжение ЦАП превысило входное напряжение (компаратор = 1)
            if comparator_output == 1:
                if self.verbose:
                    print(f"Напряжение превышено при числе: {number}")
                return number
        
        # Если не превысили - возвращаем максимальное значение
        if self.verbose:
            print(f"Достигнут максимум: {max_value}")
        return max_value
    
    def get_sc_voltage(self):
        """Возвращает измеренное напряжение в Вольтах"""
        digital_value = self.sequential_counting_adc()
        max_digital = 2**len(self.bits_gpio) - 1  # 255 для 8 бит
        
        # Преобразуем цифровое значение в напряжение
        voltage = (digital_value / max_digital) * self.dynamic_range
        
        if self.verbose:
            print(f"Цифровое значение: {digital_value}, Напряжение: {voltage:.3f} В")
        
        return voltage


# Основной охранник
if __name__ == "__main__":
    try:
        # Создаем объект АЦП (динамический диапазон нужно измерить мультиметром!)
        # Например, для 3.3В питания: dynamic_range=3.3
        adc = R2R_ADC(dynamic_range=3.3, verbose=True)
        
        # Бесконечный цикл измерений
        while True:
            # Читаем напряжение
            voltage = adc.get_sc_voltage()
            
            # Печатаем в терминал
            print(f"Измеренное напряжение: {voltage:.3f} В")
            
            # Пауза между измерениями
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    finally:
        # Вызываем деструктор
        if 'adc' in locals():
            adc.__del__()
        print("Программа завершена, GPIO очищен")