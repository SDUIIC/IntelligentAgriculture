# -*- coding: utf-8 -*-
import codecs
import json
import multiprocessing
import os
import re
import time

import Adafruit_DHT
import RPi.GPIO as GPIO
import aliyunsdkiotclient.AliyunIotMqttClient as iot

options={}
f_list = os.listdir('./')
for i in f_list:
    if (re.search('deviceinfo_',i)!=None) & (re.search('.json',i)!=None):
        with codecs.open(i, 'r','utf-8') as file:
            options = json.load(file)

productKey=str(options['productKey'])
deviceName=str(options['deviceName'])
deviceSecret=str(options['deviceSecret'])
dht_pin = options['dht_pin']
switch_pin = options['switch_pin']

switch_pin_1 = options['switch_pin_1']
switch_pin_2 = options['switch_pin_2']
switch_pin_3 = options['switch_pin_3']
switch_pin_4 = options['switch_pin_4']
switch_pin_5 = options['switch_pin_5']
switch_pin_6 = options['switch_pin_6']
switch_pin_7 = options['switch_pin_7']
switch_pin_8 = options['switch_pin_8']

HOST = productKey + '.iot-as-mqtt.cn-shanghai.aliyuncs.com'
PORT = 1883
PUB_TOPIC = "/sys/" + productKey + "/" + deviceName + "/thing/event/property/post"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_pin, GPIO.OUT)

GPIO.setup(switch_pin_1, GPIO.OUT)
GPIO.setup(switch_pin_2, GPIO.OUT)
GPIO.setup(switch_pin_3, GPIO.OUT)
GPIO.setup(switch_pin_4, GPIO.OUT)
GPIO.setup(switch_pin_5, GPIO.OUT)
GPIO.setup(switch_pin_6, GPIO.OUT)
GPIO.setup(switch_pin_7, GPIO.OUT)
GPIO.setup(switch_pin_8, GPIO.OUT)

# DHT model
def get_DHT():
    H, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht_pin)
    if H is not None and T is not None:
        return T, H
    else:
        print("==worng data==")
        return 20, 60  # default fake value


# check the message
def on_message(client, userdata, msg):
    print("==switch_message==")
    print(msg.payload)
    setjson = json.loads(msg.payload)
    led = setjson['params']['PowerSwitch']  # get the current value of PowerSwitch
    GPIO.output(switch_pin, (GPIO.HIGH if led == 1 else GPIO.LOW))

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


def on_connect(client, userdata, flags_dict, rc):
    print("Connected with result code " + str(rc))

def on_disconnect(client, userdata, flags_dict, rc):
    print("Disconnected.")

def get_client():
    return

def worker(client):
    while True:
        time.sleep(5)  # every 5 second send message
        T, H = get_DHT()
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
        client.publish(PUB_TOPIC, payload=str(payload_json))

if __name__ == '__main__':
    client = iot.getAliyunIotMqttClient(productKey, deviceName, deviceSecret, secure_mode=3)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    client.connect(host=HOST, port=PORT, keepalive=60)

    p = multiprocessing.Process(target=worker, args=(client,))
    p.start()
    client.loop_forever()
