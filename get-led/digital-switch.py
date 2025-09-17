import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
botton = 13
GPIO.setup(botton, GPIO.IN)
state = 0
while True:
    if GPIO.input(botton):
        state = 1 - state 
        GPIO.output(led, state)
        time.sleep(0.2)