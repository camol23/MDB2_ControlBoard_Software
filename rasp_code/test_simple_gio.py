#import the GPIO and time package


import RPi.GPIO as GPIO
import time

time_val = 1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(5, GPIO.OUT)

# loop through 50 times, on/off for 1 second
for i in range(50):
    GPIO.output(5,True)
    time.sleep(time_val)
    GPIO.output(5,False)
    time.sleep(time_val)


GPIO.cleanup()

