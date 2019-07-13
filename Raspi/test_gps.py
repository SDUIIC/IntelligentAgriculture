# -*- coding: utf-8 -*-

import serial
import pynmea2

def parseGPS(str):
    if str.find('GGA') > 0:
        msg=pynmea2.parse(str)
        print()


str=serial.readline()
parseGPS(str)


