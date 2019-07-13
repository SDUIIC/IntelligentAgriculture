# -*- coding: utf-8 -*-
import Adafruit_DHT
import sys

# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor=Adafruit_DHT.DHT11

# Set GPIO sensor is connected to
dht_pin=int(sys.argv[1])

# Use read_retry method. This will retry up to 15 times to
# get a sensor reading (waiting 2 seconds between each retry).
# humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

# Reading the DHT11 is very sensitive to timings and occasionally
# the Pi might fail to get a valid reading. So check if readings are valid.
def get_DHT():
    H, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht_pin)
    if H is not None and T is not None:
        return T, H
    else:
        print("wrong")
        return 20, 60  # default fake value

print(get_DHT())