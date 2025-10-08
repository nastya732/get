import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)

dynamic_range = 3.16
gpio_bits = [16, 20,21,25,26,17,27,22]

class R2R_DAC:
    def __init__(self,gpio_bits,dynamic_range,verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_bits, GPIO.OUT, initial = 0)
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
    def set_number(self, number):
        GPIO.output(gpio_bits, self.number_to_dac(number))
        print(f"Число на вход ЦАП: {number}, биты: {self.number_to_dac(number)}")
    def set_voltage(self, voltage):
        if not(0.0<=voltage<=dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00-{dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            number = 0
            self.set_number(number)
            return 0
        self.set_number((int(voltage/dynamic_range * 255)))
    def voltage_to_number(self, voltage):
        return int(voltage/dynamic_range * 255)
    def number_to_dac(self, number):
        return [int(element) for element in bin(number)[2:].zfill(8)]
if __name__ == "__main__":
    try:
        dac = R2R_DAC(gpio_bits, dynamic_range, True)
        while True:
            try:
                voltage = float(input("Введите напряжение в вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
    finally:
        dac.deinit()