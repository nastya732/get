import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

dynamic_range = 3.16
gpio_pin = 12
pwm_frequency = 500


class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose = False):
        self.gpio_pin = gpio_pin
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.pwm_frequency = pwm_frequency
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency) # Создали объект ШИМ
        self.pwm.start(0) # ← ЗАПУСТИЛИ ШИМ с 0% заполнения  Теперь ШИМ АКТИВЕН, готов к управлению
    def deinit(self):
        GPIO.output(self.gpio_pin, 0)
        GPIO.cleanup()
    def set_voltage(self, voltage):
        self.pwm.ChangeDutyCycle(voltage/self.dynamic_range*100) #Теперь ШИМ генерирует сигнал с каким-то заполнения
if __name__ == "__main__":
    try:
        dac = PWM_DAC(gpio_pin, pwm_frequency, dynamic_range, True)
        while True:
            try:
                voltage = float(input("Введите напряжение в вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
    finally:
        dac.deinit()