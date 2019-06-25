#!/usr/bin/python

import sys, time, requests, json, Adafruit_DHT, os, re, warnings, argparse

warnings.filterwarnings("ignore")

parser=argparse.ArgumentParser(description="Python script for sending live temperature and humidity data to EdgeX Foundry")
parser.add_argument('-ip',help='EdgeX Foundry IP address', required=True)
args=vars(parser.parse_args())
edgex_ip=args["ip"]


while True:
    rawHum, rawTmp = Adafruit_DHT.read_retry(11, 4)

    url = 'http://%s:48080/api/v1/event' % edgex_ip
    formHum = int(rawHum)
    strHum = str(formHum)
    formTmp = int(rawTmp)
    strTmp = str(rawTmp)
    payload = {"device":"Temp_and_Humidity_sensor_cluster_01","readings":[{"name":"Humidity","value":strHum},{"name":"Temperature in C","value":strTmp}]}
    headers = {'content-type': 'application/json'}

    if(formHum < 100):
        response = requests.post(url, data=json.dumps(payload), headers=headers,verify=False)
        print('Temp: {} C, Humidity: {} %').format(strTmp, strHum)

    #print response
    #print payload

    time.sleep(2)
