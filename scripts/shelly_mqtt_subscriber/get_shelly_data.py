#!/usr/bin/env python3
import time
# import datetime
from datetime import datetime
import paho.mqtt.client as mqtt
import json
import os
import pprint
import sys

dataset = {'energy': None, 'power': None, 'temp': None, 'relay': None}


class ShellyDataset:
    def __init__(self):
        self.data = {'energy': None, 'power': None, 'temp': None, 'relay': None}

    def checkDataset(self):
        # print("Prüfung der Werte")
        if ( self.data['energy'] is not None ) and \
                ( self.data['power'] is not None ) and \
                ( self.data['temp'] is not None ) and \
                ( self.data['relay'] is not None ):
            return True
        else:
            return False

    def test_addFullDataSet(self):
        spma.data['energy'] = "energie"
        spma.data['power'] = "power"
        spma.data['temp'] = "temp"
        spma.data['relay'] = "relay"

    def resetData(self):
        self.__init__()
        print(self.__dict__)

def on_energy(client, userdata, message):
    msg = message.payload.decode("utf-8")
    m_decode = json.loads(msg)
    spma.data['energy'] = m_decode
    # print ("energy Message received: "  + str(m_decode))

def on_power(client, userdata, message):
    msg = message.payload.decode("utf-8")
    m_decode = json.loads(msg)
    spma.data['power'] = m_decode
    # print ("power Message received: "  + str(m_decode))

def on_temperature(client, userdata, message):
    msg = message.payload.decode("utf-8")
    m_decode = json.loads(msg)
    spma.data['temp'] = m_decode
    # print ("temperature Message received: "  + str(m_decode))

def on_relay(client, userdata, message):
    msg = message.payload.decode("utf-8")
    spma.data['relay'] = str(msg)
    # print ("relay Message received: "  + str(m_decode))

os.chdir(os.path.dirname(__file__))
with open(os.getcwd() + "/config.json") as json_config_file:
    config_data = json.load(json_config_file)
mqtt_host = config_data['mqtt']['host']
mqtt_user = config_data['mqtt']['user']
mqtt_pass = config_data['mqtt']['pass']

broker_address = mqtt_host
mqtt_client = mqtt.Client("backend.shemhazai.de")
mqtt_client.connect(broker_address)
mqtt_client.subscribe("shellies/spuelmaschine/#")

mqtt_client.message_callback_add('shellies/spuelmaschine/relay/0/energy', on_energy)
mqtt_client.message_callback_add('shellies/spuelmaschine/relay/0/power', on_power)
mqtt_client.message_callback_add('shellies/spuelmaschine/temperature', on_temperature)
mqtt_client.message_callback_add('shellies/spuelmaschine/relay/0', on_relay)

spma = ShellyDataset()
while True:
    mqtt_client.loop_start()
    time.sleep(0.1)
    if spma.checkDataset() == True:
        print("Schreibe in DB: {}".format(spma.__dict__))
        spma.resetData()

    mqtt_client.loop_stop()
