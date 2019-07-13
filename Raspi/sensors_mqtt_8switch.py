# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
import hashlib
import hmac

import Adafruit_DHT
import RPi.GPIO as GPIO
import json
import os
import re

options={}
f_list = os.listdir('./')
for i in f_list:
    if (re.search('deviceinfo_',i)!=None) & (re.search('.json',i)!=None):
        with open(i, 'r') as file:
            options = json.load(file)

dht_pin =options['dht_pin']
switch_pin = options['switch_pin']

switch_pin_1 = options['switch_pin_1']
switch_pin_2 = options['switch_pin_2']
switch_pin_3 = options['switch_pin_3']
switch_pin_4 = options['switch_pin_4']
switch_pin_5 = options['switch_pin_5']
switch_pin_6 = options['switch_pin_6']
switch_pin_7 = options['switch_pin_7']
switch_pin_8 = options['switch_pin_8']

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_pin_1, GPIO.OUT)
GPIO.setup(switch_pin_2, GPIO.OUT)
GPIO.setup(switch_pin_3, GPIO.OUT)
GPIO.setup(switch_pin_4, GPIO.OUT)
GPIO.setup(switch_pin_5, GPIO.OUT)
GPIO.setup(switch_pin_6, GPIO.OUT)
GPIO.setup(switch_pin_7, GPIO.OUT)
GPIO.setup(switch_pin_8, GPIO.OUT)

HOST = options['productKey'] + '.iot-as-mqtt.cn-shanghai.aliyuncs.com'
PORT = 1883
PUB_TOPIC = "/sys/" + options['productKey'] + "/" + options['deviceName'] + "/thing/event/property/post"

# DHT model
def get_DHT():
    H, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht_pin)
    if H is not None and T is not None:
        return T, H
    else:
        return 20, 60  # default fake value

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_disconnect(client, userdata, flags_dict, rc):
    print("Disconnected.")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    setjson = json.loads(msg.payload)

    PowerSwitch = setjson['params']['PowerSwitch']  # get the current value of PowerSwitch
    GPIO.output(switch_pin, (GPIO.HIGH if PowerSwitch == 1 else GPIO.LOW))

    PowerSwitch_1 = setjson['params']['PowerSwitch_1']  # get the current value of PowerSwitch
    GPIO.output(switch_pin_1, (GPIO.HIGH if PowerSwitch_1 == 1 else GPIO.LOW))

    PowerSwitch_2 = setjson['params']['PowerSwitch_2']  # get the current value of PowerSwitch
    GPIO.output(switch_pin_2, (GPIO.HIGH if PowerSwitch_2 == 1 else GPIO.LOW))

    PowerSwitch_3 = setjson['params']['PowerSwitch_3']  # get the current value of PowerSwitch
    GPIO.output(switch_pin_3, (GPIO.HIGH if PowerSwitch_3 == 1 else GPIO.LOW))

    PowerSwitch_4 = setjson['params']['PowerSwitch_4']  # get the current value of PowerSwitch
    GPIO.output(switch_pin_4, (GPIO.HIGH if PowerSwitch_4 == 1 else GPIO.LOW))

    PowerSwitch_5 = setjson['params']['PowerSwitch_5']  # get the current value of PowerSwitch
    GPIO.output(switch_pin_5, (GPIO.HIGH if PowerSwitch_5 == 1 else GPIO.LOW))

    PowerSwitch_6 = setjson['params']['PowerSwitch_6']  # get the current value of PowerSwitch
    GPIO.output(switch_pin_6, (GPIO.HIGH if PowerSwitch_6 == 1 else GPIO.LOW))

    PowerSwitch_7 = setjson['params']['PowerSwitch_7']  # get the current value of PowerSwitch
    GPIO.output(switch_pin_7, (GPIO.HIGH if PowerSwitch_7 == 1 else GPIO.LOW))

    PowerSwitch_8 = setjson['params']['PowerSwitch_8']  # get the current value of PowerSwitch
    GPIO.output(switch_pin_8, (GPIO.HIGH if PowerSwitch_8 == 1 else GPIO.LOW))

def hmacsha1(key, msg):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha1).hexdigest()

# get client
def getAliyunIoTClient():
    timestamp = str(int(time.time()))
    CLIENT_ID = "paho.py|securemode=3,signmethod=hmacsha1,timestamp=" + timestamp + "|"
    CONTENT_STR_FORMAT = "clientIdpaho.pydeviceName" + options['deviceName'] + "productKey" + options[
        'productKey'] + "timestamp" + timestamp
    # set username/password.
    USER_NAME = options['deviceName'] + "&" + options['productKey']
    PWD = hmacsha1(options['deviceSecret'], CONTENT_STR_FORMAT)
    client = mqtt.Client(client_id=CLIENT_ID, clean_session=False)
    client.username_pw_set(USER_NAME, PWD)
    return client

def worker(client):
    while True:
        time.sleep(5)  # every 5 second send message
        T, H = get_DHT()
        if T != 0 or H != 0:
            payload_json = {
                'id': int(time.time()),
                'params': {
                    'temperature': T,  # random.randint(20, 30),
                    'humidity': H,  # random.randint(40, 50)
                    'switch_starttime': '2019-07-12 09:00:00',
                    'switch_endtime': '2019-07-15 10:00:00'
                },
                'method': "thing.event.property.post"
            }

            print('==client== send data to iot server: ' + str(payload_json))
            client.publish(PUB_TOPIC, payload=str(payload_json), qos=1)


if __name__ == '__main__':
    client = getAliyunIoTClient()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.on_message = on_message
    client.connect(HOST, PORT, 300)

    worker(client)

    client.loop_forever()