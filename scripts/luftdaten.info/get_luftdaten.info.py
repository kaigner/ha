#!/usr/bin/env python3

import time
from datetime import datetime
import pymysql
import json
import logging
import urllib.request
import json
import os
import sys

dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
json_values = {}

os.chdir(os.path.dirname(__file__))

# Read Config File
with open(os.getcwd() + "/config.json") as json_config_file:
        config_data=json.load(json_config_file)
db_host  = config_data['mysql']['host']
db_user  = config_data['mysql']['user']
db_pass  = config_data['mysql']['pass']
db_name  = config_data['mysql']['db']
device   = config_data['sensor']['type']
alias    = config_data['sensor']['alias']
vendor   = config_data['sensor']['vendor']
place    = config_data['sensor']['location']
ip       = config_data['sensor']['ip']
readings = config_data['sensor']['readings']
sensors  = config_data['sensor']['sensors']


# get data from device
devurl = "http://" + ip + "/data.json"
with urllib.request.urlopen(devurl) as url:
       data = json.loads(url.read().decode())

# map data
for _data in data['sensordatavalues']:
    # print(_data)
    # print("{} :  {}".format(_data['value_type'],  _data['value']))
    json_values[_data['value_type']] = _data['value']
    if _data['value_type'] == "SDS_P1":
        pm10 = _data['value']
    if _data['value_type'] == "SDS_P2":
        pm25 = _data['value']
    if _data['value_type'] == "BME280_temperature":
        temp = _data['value']
    if _data['value_type'] == "BME280_pressure":
        hpa = _data['value']
    if _data['value_type'] == "BME280_humidity":
        humidity = _data['value']
    if _data['value_type'] == "signal":
        signal = _data['value']
    if _data['value_type'] == "samples":
        samples = _data['value']

# print("pm10: {} pm25: {} temp: {} hum: {} hpa {} sig: {}".format(pm10, pm25, temp, humidity, hpa, signal))

try:
	db = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
except pymysql.err.OperationalError as error:
	print("- error connecting to database: {}".format(error))
	sys.exit(1)
cursor = db.cursor()

# if (db):
    # True:
# else:
    # logger.critical("Datenbankversbingung FEHLER")
    # sys.exit(0)

cursor = db.cursor()
sql = "INSERT INTO feinstaub_daten (timestamp, device, alias, vendor, sensors, location, pm10, pm2_5, temp, humidity, airpressure, sig, json_data) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
cursor.execute(sql, (dt, device, alias, vendor, str(sensors), place, float(pm10), float(pm25), float(temp), float(humidity), float(hpa), int(signal), json.dumps(json_values)))
db.commit()
db.close()
