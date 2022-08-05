#!/usr/bin/env python3
import time
# import datetime
from datetime import datetime
import paho.mqtt.client as mqtt
import json
import os
# import pprint
import sys
import pymysql
import hashlib


class ShellyDataset:
    def __init__(self):
        self.data = {'energy': None, 'power': None, 'temp': None, 'relay': None}
        self.prev_Checksum = 0

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

    def genChecksum(self):
        self.data['temp']=round(self.data['temp'],1)
        return hashlib.md5(str(self.__dict__).encode('utf-8')).hexdigest()

    def genPreviewsChecksum(self):
        return hashlib.md5(str(self.__dict__).encode('utf-8')).hexdigest()

    def addDataToDB(self):
        sql = "INSERT INTO common_data (device, type, event, reading, json_data, unit) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql,(dev, dev_type, "update", "data", json.dumps(self.data), "json" ))
        db.commit()

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

try:
    with open(os.getcwd() + "/config.json") as json_config_file:
        config_data = json.load(json_config_file)
except FileNotFoundError as error:
    print("- config file not found, exit: {}".format(error))
    sys.exit(1)

try:
    mqtt_host = config_data['mqtt']['host']
    mqtt_user = config_data['mqtt']['user']
    mqtt_pass = config_data['mqtt']['pass']
    db_host = config_data['database']['db_host']
    db_name = config_data['database']['db_name']
    db_user = config_data['database']['db_user']
    db_pass = config_data['database']['db_pass']
    dev = config_data['device']['dev']
    dev_type = config_data['device']['dev_type']
except KeyError as error:
    print("- value mapping from config not ok: {}".format(error))
    sys.exit(1)

try:
    db = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
except pymysql.err.OperationalError as error:
    print("- error connecting to database: {}".format(error))
    sys.exit(1)
cursor = db.cursor()

broker_address = mqtt_host
mqtt_client = mqtt.Client("backend.shemhazai.de")
mqtt_client.connect(broker_address)
mqtt_client.subscribe("shellies/spuelmaschine/#")

mqtt_client.message_callback_add('shellies/spuelmaschine/relay/0/energy', on_energy)
mqtt_client.message_callback_add('shellies/spuelmaschine/relay/0/power', on_power)
mqtt_client.message_callback_add('shellies/spuelmaschine/temperature', on_temperature)
mqtt_client.message_callback_add('shellies/spuelmaschine/relay/0', on_relay)

spma = ShellyDataset()
prev_Checksum = 0
while True:
    mqtt_client.loop_start()
    time.sleep(0.1)

    if spma.checkDataset() == True:
        act_checksum = spma.genChecksum()
        # print("act: {} prev {}".format(act_checksum, prev_Checksum))
        if prev_Checksum != act_checksum:
            spma.addDataToDB()
            prev_Checksum = spma.genPreviewsChecksum()
        else:
            pass
        spma.resetData()

    mqtt_client.loop_stop()
