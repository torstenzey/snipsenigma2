#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import json
import httplib

def on_connect(client, userdata, flags, rc):
    mqtt.subscribe('hermes/intent/torstenzey:television_on')
    mqtt.subscribe('hermes/intent/torstenzey:television_off')
    mqtt.subscribe('hermes/intent/torstenzey:volume_down')
    mqtt.subscribe('hermes/intent/torstenzey:volume_up')
    mqtt.subscribe('hermes/intent/torstenzey:zap_forward')
    mqtt.subscribe('hermes/intent/torstenzey:zap_backward')
def on_message(client, userdata, msg):
    # Parse the json response
    intent_json = json.loads(msg.payload)
    intentName = intent_json['intent']['intentName']
    slots = intent_json['slots']
    print('Intent {}'.format(intentName))

    con = httplib.HTTPConnection('192.168.178.206')
    if 'torstenzey:television_on' == intentName :
        con.request("GET", "/web/powerstate?newstate=4")
    elif 'torstenzey:television_off' == intentName :
        con.request("GET", "/web/powerstate?newstate=5")
    elif 'torstenzey:volume_down' == intentName :
        con.request("GET", "/web/vol?set=down")
    elif 'torstenzey:volume_up' == intentName :
        con.request("GET", "/web/vol?set=up")
    elif 'torstenzey:zap_forward' == intentName :
        con.request("GET", "/web/remotecontrol?command=407")
    elif 'torstenzey:zap_forward' == intentName :
        con.request("GET", "/web/remotecontrol?command=412")

    print(con.getresponse().status)

    con.close()
    
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
