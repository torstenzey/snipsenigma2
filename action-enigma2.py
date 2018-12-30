#!/usr/bin/env python2
 
import sys
import paho.mqtt.client as mqtt
from hermes_python.hermes import Hermes

def intent_received(_self, hermes, intent_message):
    print('Intent {}'.format(intent_message.intent))
    
    for (slot_value, slot) in intent_message.slots.items():
        print('Slot {} -> \n\tRaw: {} \tValue: {}'.format(slot_value, slot[0].raw_value, slot[0].slot_value.value.value))

    hermes.publish_end_session(intent_message.session_id, None)
    
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("hermes/hotword/default/detected")
    # Subscribe to intent topic
    client.subscribe("hermes/intent/#")
        

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
