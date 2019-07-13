# -*- coding: utf-8 -*-
import aliyunsdkiotclient.AliyunIotMqttClient as iot
import json
import multiprocessing
import time
import random
import RPi.GPIO as GPIO
import Adafruit_DHT

options = {
    'productKey': 'a1aJ8m9TiRL',
    'deviceName': '00IbKPRM2Ekw7HkZyaQv',
    'deviceSecret': '1sffyhL68vTYnf3qnrq56XwX7i0gR36m',
    'port': 1883,
    'host': 'iot-as-mqtt.cn-shanghai.aliyuncs.com'
}

dht_pin = 17
led_pin = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)


def GetDTH():
    H, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht_pin)
    if H is not None and T is not None:
        return T, H
    else:
        return 20, 60  # default fake value


host = options['productKey'] + '.' + options['host']


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # topic = '/' + productKey + '/' + deviceName + '/update'
    # {"method":"thing.service.property.set","id":"169885527","params":{"LED":1},"version":"1.0.0"}
    print(msg.payload)
    setjson = json.loads(msg.payload)
    led = setjson['params']['PowerSwitch']
    GPIO.output(led_pin, (GPIO.HIGH if led == 1 else GPIO.LOW))


def on_connect(client, userdata, flags_dict, rc):
    print("Connected with result code " + str(rc))


def on_disconnect(client, userdata, flags_dict, rc):
    print("Disconnected.")


def worker(client):
    topic = '/sys/' + options['productKey'] + '/' + options['deviceName'] + '/thing/event/property/post'
    while True:
        time.sleep(5)
        T, H = GetDTH()
        print 'T=', T, 'H=', H

        if T != 0 or H != 0:
            payload_json = {
                'id': int(time.time()),
                'params': {
                    'temperature': T,  # random.randint(20, 30),
                    'humidity': H,  # random.randint(40, 50)
                },
                'method': "thing.event.property.post"
            }

            print('send data to iot server: ' + str(payload_json))
            client.publish(topic, payload=str(payload_json))


if __name__ == '__main__':
    client = iot.getAliyunIotMqttClient(options['productKey'], options['deviceName'], options['deviceSecret'],
                                        secure_mode=3)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(host=host, port=options['port'], keepalive=60)

    p = multiprocessing.Process(target=worker, args=(client,))
    p.start()
    client.loop_forever()
