# -*- coding: utf-8 -*-

import requests  # 导入requests包
from bs4 import BeautifulSoup
import json


def get_datetime():

    url = 'http://121.41.19.125/proxy/javascript_simple.html'
    strhtml = requests.get(url)
    print(strhtml)


    soup = BeautifulSoup(strhtml.text, 'lxml')
    starttime = soup.select('//*[@id="starttime"]')
    endtime = soup.select('//*[@id="endtime"]')

    print(starttime)
    print(endtime)

    # return starttime, endtime


def get_datetime1():
    url = 'D:\Code\Raspi\javascript_datetimepicker.html'
    with open(url,'r') as f:
        print(f)
        # soup = BeautifulSoup(strhtml.text, 'lxml')


if __name__ == '__main__':
    # starttime, endtime = get_datetime()
    get_datetime()