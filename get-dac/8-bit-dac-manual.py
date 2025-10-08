import RPi.GPIO as GPIO
# import time

GPIO.setmode(GPIO.BCM)
pins=[16,20,21,25,26,17,27,22]
GPIO.setup(pins,GPIO.OUT)
DR=3.15 #динамический диапазон

def VoltageToNumber(voltage):
    if not(0.0<= voltage <= DR):
        print(f"напряжение выходит за динамический диапазон ЦАП (0.00 - {DR:.2f} B)")
        print("устанавливаем 0.0 B")
        return 0
    print(int(voltage/DR *255))
    return int((voltage / DR)*255)

def NumberToDac(num):
    num_bin=[int(e) for e in bin(num)[2:].zfill(8)]
    for i in range(8):
        GPIO.output(pins[i],int(num_bin[i]))
    print(num_bin)

    return 1

try: 
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = VoltageToNumber(voltage)
            NumberToDac(number)

        except ValueError:
            print("Вы ввели не числою Попробуйте еще раз\n")

finally:
    GPIO.output(pins,0)
    GPIO.cleanup()


