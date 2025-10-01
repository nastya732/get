import RPi.GPIO as GPIO

dac_pins = [16, 20, 21, 25, 26, 17, 27, 22]
# setting up these pins as output
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac_pins, GPIO.OUT)

dac_voltage_range = 3.3
def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dac_voltage_range):
        print(f"")
GPIO.setup([9, 10], GPIO.IN)
sleep_time = 0.2
up = 9
down = 10

GPIO.output(leds, 0)

num = 0

while True:
    if GPIO.input(up) > 0 and GPIO.input(down) > 0:
            num = 255
            print(num, dec2bin(num))
            time.sleep(sleep_time)
            for i in range(8):
                GPIO.output(leds[i], dec2bin(num)[i])
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
    
