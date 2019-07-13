# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
import hashlib
import hmac
import random


options = {
    'productKey': 'a1aJ8m9TiRL',
    'deviceName': 'BVQmphp1eVh9bzACwIx0',
    'deviceSecret': 'DhP6odrw5PHhkR3P9qtOlkDr95k3R0GU',
    'regionId': 'cn-shanghai'
}

HOST = options['productKey'] + '.iot-as-mqtt.' + options['regionId'] + '.aliyuncs.com'
PORT = 1883
PUB_TOPIC = "/sys/" + options['productKey'] + "/" + options['deviceName'] + "/thing/event/property/post";


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # client.subscribe("the/topic")

def on_disconnect(client, userdata, flags_dict, rc):
    print("Disconnected.")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


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
    topic = '/sys/'+options['productKey']+'/'+options['deviceName']+'/thing/event/property/post'
    while True:
        time.sleep(5) # every 5 second send message
        payload_json = {
            'id': int(time.time()),
            'params': {
                'temperature': random.randint(20, 30),
                'humidity': random.randint(40, 50)
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
    client.connect(HOST, 1883, 300)

    worker(client)

    client.loop_forever()