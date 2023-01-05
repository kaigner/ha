#!/usr/bin/python3.8

import json
import os, sys
import paho.mqtt.client as mqtt
import pymysql
from datetime import datetime

# Lese Konfig 
os.chdir(os.path.dirname(__file__))

# Read Config File
with open(os.getcwd() + "/config.json") as json_config_file:
	config_data=json.load(json_config_file)
ttn_user = config_data['ttn_auth']['user']
ttn_pass = config_data['ttn_auth']['pass']
db_host = config_data['mysql']['host']
db_user = config_data['mysql']['user']
db_pass = config_data['mysql']['pass']
db_name = config_data['mysql']['db']

# wo hängt der Counter
location = "muc-ea2-pax-1"


def addDataToDB(wifi, ble, gwname, gweui, freq, freqts, location):
	try:
		db = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
	except pymysql.err.OperationalError as error:
		print("- error connecting to database: {}".format(error))
		pass
	
	cursor = db.cursor()
	if (db):
		pass #print("Datenbankverbindung OK")
	else:
		pass
	
	dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	sql = "INSERT INTO paxdata (wifi, ble, gwname, gweui, freq, dt, location) VALUES (%s, %s, %s, %s, %s, %s, %s)"
	cursor.execute(sql,(wifi, ble, gwname, gweui, freq, dt, location))
	db.commit()
	db.close()


def on_connect(mqttc, mosq, obj,rc):
	print("Connected with result code:"+str(rc))
	# subscribe for all devices of user
	mqttc.subscribe('v3/paxcounter-munich-ea@ttn/devices/pax-counter-test-app-munich/#')


def on_message(mqttc, obj, msg):
	try:
		json_data = json.loads(msg.payload.decode('utf-8'))
		ble = json_data["uplink_message"]["decoded_payload"]["ble"]
		wifi = json_data["uplink_message"]["decoded_payload"]["wifi"]
		gw_name = json_data["uplink_message"]["rx_metadata"][0]["gateway_ids"]["gateway_id"]
		gw_eui = json_data["uplink_message"]["rx_metadata"][0]["gateway_ids"]["eui"]
		freq = json_data["uplink_message"]["settings"]["frequency"]
		freq_ts = json_data["uplink_message"]["settings"]["timestamp"]

		print("Wifi          : {} Ble: {}".format(wifi, ble))
		print("Gateway       : {} ({})".format(gw_name, gw_eui))
		print("Freq          : {}".format(str(freq)) )
		print("Freq Timestamp: {}".format(str(freq_ts)) )
		addDataToDB(wifi, ble, gw_name, gw_eui, freq, freq_ts, location)
	except Exception as e:
		print(e)
		pass


mqttc = mqtt.Client()
mqttc.on_connect=on_connect
mqttc.on_message=on_message

mqttc.username_pw_set(ttn_user, ttn_pass)
mqttc.connect("eu1.cloud.thethings.network", 1883, 60)

run = True
while run:
	mqttc.loop()
