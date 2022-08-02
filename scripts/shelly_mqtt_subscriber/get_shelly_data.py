#!/usr/bin/env python3
import time
# import datetime
from datetime import datetime
import paho.mqtt.client as mqtt
import json
import pprint
import sys

dataset = {'energy': None, 'power': None, 'temp': None, 'relay': None}


class shellyDataset:
    def __init__(self):
        self.data = {'energy': None, 'power': None, 'temp': None, 'relay': None}


# sys.exit(0)


def on_energy(client, userdata, message):
    msg = message.payload.decode("utf-8")
    m_decode = json.loads(msg)
    dataset['energy'] = m_decode


# print ("energy Message received: "  + str(m_decode))

def on_power(client, userdata, message):
    msg = message.payload.decode("utf-8")
    m_decode = json.loads(msg)
    dataset['power'] = m_decode


# print ("power Message received: "  + str(m_decode))

def on_temperature(client, userdata, message):
    msg = message.payload.decode("utf-8")
    m_decode = json.loads(msg)
    dataset['temp'] = m_decode


# print ("temperature Message received: "  + str(m_decode))

def on_relay(client, userdata, message):
    msg = message.payload.decode("utf-8")
    dataset['relay'] = str(msg)


# print ("relay Message received: "  + str(m_decode))

def check_dataset(dataset):
    # pprint.pprint(dataset)
    if (dataset['energy'] is not None) and (dataset['power'] is not None) and (dataset['temp'] is not None) and (
            dataset['relay'] is not None):
        pprint.pprint(dataset)
        # print("Set komplett ( {} - {} )".format(k, dataset[k]))
        print("db insert")
        print("Dict zuruecksetzten")
    # return {'energy':None, 'power':None, 'temp':None, 'relay':None}


broker_address = "192.168.2.15"
mqtt_client = mqtt.Client("backend.shemhazai.de")
mqtt_client.connect(broker_address)
mqtt_client.subscribe("shellies/spuelmaschine/#")

mqtt_client.message_callback_add('shellies/spuelmaschine/relay/0/energy', on_energy)
mqtt_client.message_callback_add('shellies/spuelmaschine/relay/0/power', on_power)
mqtt_client.message_callback_add('shellies/spuelmaschine/temperature', on_temperature)
mqtt_client.message_callback_add('shellies/spuelmaschine/relay/0', on_relay)

while True:
    # mqtt_client.loop_forever()
    mqtt_client.loop_start()
    dataset1 = check_dataset(dataset)
    time.sleep(0.1)
    # print(dataset)
    mqtt_client.loop_stop()
