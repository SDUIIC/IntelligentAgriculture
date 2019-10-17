# -*- coding: utf-8 -*-
import codecs
import datetime
import json
import multiprocessing
import os
import re
import time
import threading
import Adafruit_DHT
import RPi.GPIO as GPIO
import aliyunsdkiotclient.AliyunIotMqttClient as iot
import sys
from threading import Timer


sensor=Adafruit_DHT.DHT11

# Set GPIO sensor is connected to
dht_pin = 17
two_hour = 5
# Use read_retry method. This will retry up to 15 times to
# get a sensor reading (waiting 2 seconds between each retry).
# humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

# Reading the DHT11 is very sensitive to timings and occasionally
# the Pi might fail to get a valid reading. So check if readings are valid.


options={}
f_list = os.listdir('./')
for i in f_list:
    if (re.search('deviceinfo2_',i)!=None) & (re.search('.json',i)!=None):
        with codecs.open(i, 'r','utf-8') as file:
            options = json.load(file)

productKey=str(options['productKey'])
deviceName=str(options['deviceName'])
deviceSecret=str(options['deviceSecret'])
dht_pin = options['dht_pin']
#switch_pin = options['switch_pin']

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

GPIO.setup(switch_pin_1, GPIO.OUT)
GPIO.setup(switch_pin_2, GPIO.OUT)
GPIO.setup(switch_pin_3, GPIO.OUT)
GPIO.setup(switch_pin_4, GPIO.OUT)
GPIO.setup(switch_pin_5, GPIO.OUT)
GPIO.setup(switch_pin_6, GPIO.OUT)
GPIO.setup(switch_pin_7, GPIO.OUT)
GPIO.setup(switch_pin_8, GPIO.OUT)


thread_group = []



PowerSwitch = [0]*8
# DHT model
def get_DHT():
    H, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, dht_pin)
    if H is not None and T is not None:
        return T, H
    else:
        print("==worng data==")
        return 20, 60  # default fake value

def send_close_time(if_close,i):
    if if_close==1:
        payload_json = {
                'id': int(time.time()),
                'params': {
                    'PowerSwitchCloseTime_'+str(i):str(datetime.datetime.now().hour+2)+':'+str(datetime.datetime.now().minute)
                },
                'method': "thing.event.property.post"
            }
        print(payload_json)
        print("==close time==")
        client.publish(PUB_TOPIC, payload=str(payload_json))
    elif if_close==0:
        payload_json = {
            'id': int(time.time()),
            'params': {
                'PowerSwitchCloseTime_'+str(i):'XX:XX'
            },
            'method': "thing.event.property.post"
        }
        print(payload_json)
        print("==close time==")
        client.publish(PUB_TOPIC, payload=str(payload_json))

# check the message
def on_message(client, userdata, msg):
    print("==switch_message==")
    print(msg.payload)
    setjson = json.loads(msg.payload)
    if 'PowerSwitch_1' in setjson['params']:
        tmp_1 = setjson['params']['PowerSwitch_1']
        if tmp_1 == 1:
            thread_group[0]=threading.Timer(two_hour, close, args=(switch_pin_1,1))    
            thread_group[0].start()
            PowerSwitch[0] = 1
            GPIO.output(switch_pin_1, GPIO.HIGH)
            send_close_time(1,1)
        elif tmp_1 == 0:  
            GPIO.output(switch_pin_1,GPIO.LOW)
            send_close_time(0,1)
            if PowerSwitch[0] == 1:
                PowerSwitch[0] = 0
                thread_group[0].cancel()
    elif 'PowerSwitch_2' in setjson['params']:
        tmp_2 = setjson['params']['PowerSwitch_2']       
        if tmp_2 == 1:      
            thread_group[1]=threading.Timer(two_hour, close, args=(switch_pin_2,2))  
            thread_group[1].start()
            PowerSwitch[1] = 1
            GPIO.output(switch_pin_2, GPIO.HIGH)
            send_close_time(1,2)
        elif tmp_2 == 0:
            send_close_time(0,2)
            GPIO.output(switch_pin_2,GPIO.LOW)
            if PowerSwitch[1] == 1:
                PowerSwitch[1] = 0
                thread_group[1].cancel()
    elif 'PowerSwitch_3' in setjson['params']:
        tmp_3 = setjson['params']['PowerSwitch_3']       
        if tmp_3 == 1:      
            thread_group[2]=threading.Timer(two_hour, close, args=(switch_pin_3,3))    
            thread_group[2].start()
            PowerSwitch[2] = 1
            GPIO.output(switch_pin_3, GPIO.HIGH)
            send_close_time(1,3)
        elif tmp_3 == 0:
            send_close_time(0,3)
            GPIO.output(switch_pin_3,GPIO.LOW)
            if PowerSwitch[2] == 1:
                PowerSwitch[2] = 0
                thread_group[2].cancel()
    elif 'PowerSwitch_4' in setjson['params']:
        tmp_4 = setjson['params']['PowerSwitch_4']       
        if tmp_4 == 1:      
            thread_group[3]=threading.Timer(two_hour, close, args=(switch_pin_4,4))    
            thread_group[3].start()
            PowerSwitch[3] = 1
            GPIO.output(switch_pin_4, GPIO.HIGH)
            send_close_time(1,4)
        elif tmp_4 == 0:
            send_close_time(0,4)
            GPIO.output(switch_pin_4,GPIO.LOW)
            if PowerSwitch[3] == 1:
                PowerSwitch[3] = 0
                thread_group[3].cancel()
    elif 'PowerSwitch_5' in setjson['params']:
        tmp_5 = setjson['params']['PowerSwitch_5']       
        if tmp_5 == 1:      
            thread_group[4]=threading.Timer(two_hour, close, args=(switch_pin_5,5))    
            thread_group[4].start()
            PowerSwitch[4] = 1
            GPIO.output(switch_pin_5, GPIO.HIGH)
            send_close_time(1,5)
        elif tmp_5 == 0:
            send_close_time(0,5)
            GPIO.output(switch_pin_5,GPIO.LOW)
            if PowerSwitch[4] == 1:
                PowerSwitch[4] = 0
                thread_group[4].cancel()
    elif 'PowerSwitch_6' in setjson['params']:
        tmp_6 = setjson['params']['PowerSwitch_6']       
        if tmp_6 == 1:      
            thread_group[5]=threading.Timer(two_hour, close, args=(switch_pin_6,6))    
            thread_group[5].start()
            PowerSwitch[5] = 1
            GPIO.output(switch_pin_6, GPIO.HIGH)
            send_close_time(1,6)
        elif tmp_6 == 0:
            send_close_time(0,6)
            GPIO.output(switch_pin_6,GPIO.LOW)
            if PowerSwitch[5] == 1:
                PowerSwitch[5] = 0
                thread_group[5].cancel()
    elif 'PowerSwitch_7' in setjson['params']:
        tmp_7 = setjson['params']['PowerSwitch_7']       
        if tmp_7 == 1:      
            thread_group[6]=threading.Timer(two_hour, close, args=(switch_pin_7,7))    
            thread_group[6].start()
            PowerSwitch[6] = 1
            GPIO.output(switch_pin_7, GPIO.HIGH)
            send_close_time(1,7)
        elif tmp_7 == 0:
            send_close_time(0,7)
            GPIO.output(switch_pin_7,GPIO.LOW)
            if PowerSwitch[6] == 1:
                PowerSwitch[6] = 0
                thread_group[6].cancel()
    elif 'PowerSwitch_8' in setjson['params']:
        tmp_8 = setjson['params']['PowerSwitch_8']       
        if tmp_8 == 1:      
            thread_group[7]=threading.Timer(two_hour, close, args=(switch_pin_8,8))    
            thread_group[7].start()
            PowerSwitch[7] = 1
            GPIO.output(switch_pin_8, GPIO.HIGH)
            send_close_time(1,8)
        elif tmp_8 == 0:
            send_close_time(0,8)
            GPIO.output(switch_pin_8,GPIO.LOW)
            if PowerSwitch[7] == 1:
                PowerSwitch[7] = 0
                thread_group[7].cancel()
    print("==switch_message over==")

def close(switch_pin,i):
    GPIO.output(switch_pin,GPIO.LOW)
    PowerSwitch[i] = 0
    payload_json = {
            'id': int(time.time()),
            'params': {
                'PowerSwitch_'+str(i): 0,
                'PowerSwitchCloseTime_'+str(i):'XX:XX'
            },
            'method': "thing.event.property.post"
        }
    print(payload_json)
    print("==close over==")
    client.publish(PUB_TOPIC, payload=str(payload_json))
def on_connect(client, userdata, flags_dict, rc):
    print("Connected with result code " + str(rc))

def on_disconnect(client, userdata, flags_dict, rc):
    print("Disconnected.")

def get_client():
    return

def worker(client):
    while True:
        time.sleep(2)  # every 5 second send message
        a,b = get_DHT()
        a = int(a)
        b = int(b)
        payload_json = {
            'id': int(time.time()),
            'params': {
                'CurrentTemperature_1': a,
                'RelativeHumidity_1': b
            },
            'method': "thing.event.property.post"
        }
        print('==client== send data to iot server ')
        print(payload_json)
        client.publish(PUB_TOPIC, payload=str(payload_json))
        print("==client_message over==")
def camera():
    os.system('./CameraUSB.sh')


if __name__ == '__main__':
    client = iot.getAliyunIotMqttClient(productKey, deviceName, deviceSecret, secure_mode=3)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(host=HOST, port=PORT, keepalive=60)
    thread_group.append(threading.Timer(two_hour, close, args=(switch_pin_1,1)))
    thread_group.append(threading.Timer(two_hour, close, args=(switch_pin_2,2)))
    thread_group.append(threading.Timer(two_hour, close, args=(switch_pin_3,3)))
    thread_group.append(threading.Timer(two_hour, close, args=(switch_pin_4,4)))
    thread_group.append(threading.Timer(two_hour, close, args=(switch_pin_5,5)))
    thread_group.append(threading.Timer(two_hour, close, args=(switch_pin_6,6)))
    thread_group.append(threading.Timer(two_hour, close, args=(switch_pin_7,7)))
    thread_group.append(threading.Timer(two_hour, close, args=(switch_pin_8,8)))
    #q = multiprocessing.Process(target=camera)
    p = multiprocessing.Process(target=worker, args=(client,))
    #q.start()
    p.start()
    client.loop_forever()
