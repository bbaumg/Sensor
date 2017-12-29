import RPi.GPIO as GPIO
from time import sleep

# The script as below using BCM GPIO 00..nn numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set relay pins as output
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
#GPIO.setup(24, GPIO.OUT)
#GPIO.setup(25, GPIO.OUT)

while (True):
    GPIO.output(5, GPIO.HIGH)
    sleep(.5)
    GPIO.output(6, GPIO.HIGH)
    #GPIO.output(24, GPIO.HIGH)
    #GPIO.output(25, GPIO.HIGH)
    # Sleep for 5 seconds
    sleep(1) 
    # Turn all relays OFF
    GPIO.output(5, GPIO.LOW)
    sleep(.5)
    GPIO.output(6, GPIO.LOW)
    #GPIO.output(24, GPIO.LOW)
    #GPIO.output(25, GPIO.LOW)   
    # Sleep for 5 seconds
    sleep(1)

