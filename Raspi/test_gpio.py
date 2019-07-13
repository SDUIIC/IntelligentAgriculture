# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import sys
import time

pin = int(sys.argv[1])
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

while True:
    print 'HIGH'
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(2)

    print 'LOW'
    GPIO.output(pin, GPIO.LOW)
    time.sleep(2)

GPIO.cleanup()


