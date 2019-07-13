# 智能农业-IIC开发

## 说明
所包含的程序使用说明

+ test 开头的文件是测试脚本
+ sensors 开头的文件是正式运行程序
+ deviceinfo 开头的文件是阿里云提供的设备码，一台设备只能有一个这样的文件
+ Camera 开头文件是启动摄像头进行监控的脚本文件


## test 文件
``` python test_DHT11.py [dht11_pin] ```
运行该文件需要加入树莓派上链接dht11传感器的引脚BCM编号, 若测试成功则会输出当前的温度和湿度

` python test_DHT22.py [dht22_pin] `
运行该文件需要加入树莓派上链接dht11传感器的引脚BCM编号, 若测试成功则会输出当前的温度和湿度

` python test_gpio.python [pin] `
pin为需要测试的GPIO编号，程序每2s变换pin的高低电平

` python test_aliyun.py `
在程序中编写好设备码，和需要向阿里云传输的键值对，测试与阿里云是否能狗传递消息

## deviceinfo.json 文件
在阿里云的项目管理中，找到具体设备的key值，填入该json文件。
设置好传感器和开关的引脚

## sensors 文件
两类与阿里云的通信方式
+ aliyun : 是通过aliyunsdkiotclient.AliyunIotMqttClient包通信
+ mqtt : 是通过paho.mqtt.client包通信

开关数量
+ 1switch : 只有一个开关可控，变量名为PowerSwitch，json文件里和阿里云都是这个名字
+ 8switch : 8个可控开关，变量名为PowerSwitch_1 ~ PowerSwitch_1

## Camera 文件
+ CameraPi：使用Pi Camera 树莓派原生摄像头
+ CameraUSB：使用USB Camera USB摄像头

