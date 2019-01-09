#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import json
import httplib

def on_connect(client, userdata, flags, rc):
    print('Connected')
    mqtt.subscribe('hermes/intent/torstenzey:FernseherAn')
def on_message(client, userdata, msg):
    # Parse the json response
    intent_json = json.loads(msg.payload)
    intentName = intent_json['intent']['intentName']
    slots = intent_json['slots']
    print('Intent {}'.format(intentName))

    con = httplib.HTTPConnection('192.168.178.206')
    print('1')
    con.request("GET", "/web/powerstate?newstate=0")
    print(con.getresponse().status)

    for slot in slots:
        slot_name = slot['slotName']
        raw_value = slot['rawValue']
        value = slot['value']['value']
        print('Slot {} -> \n\tRaw: {} \tValue: {}'.format(slot_name, raw_value, value))

mqtt = mqtt.Client()
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.connect('127.0.0.1', 1883)
mqtt.loop_forever()
