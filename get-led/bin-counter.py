import RPi.GPIO as GPIO
import time
def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

GPIO.setmode(GPIO.BCM)

leds = [16, 12, 25, 17, 27, 23, 22, 24]
GPIO.setup(leds, GPIO.OUT)
GPIO.setup([9, 10], GPIO.IN)
sleep_time = 0.2
up = 9
down = 10

GPIO.output(leds, 0)

num = 0

while True:
    if GPIO.input(up) > 0:
        if num < 255:
            num += 1
            print(num, dec2bin(num))
            time.sleep(sleep_time)
        for i in range(8):
            GPIO.output(leds[i], dec2bin(num)[i])
    if GPIO.input(down) > 0:
        if num > 0:
            num -= 1
            print(num, dec2bin(num))
            time.sleep(sleep_time)

        for i in range(8):
            GPIO.output(leds[i], dec2bin(num)[i])
    
