#!/usr/bin/env python3

import time
from datetime import datetime
import psycopg2  # PostgreSQL-Connector
import json
import urllib.request
import os
import sys

dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

os.chdir(os.path.dirname(__file__))

# Read Config File
with open(os.getcwd() + "/config-psql-muc.json") as json_config_file:
    config_data = json.load(json_config_file)

db_host = config_data['postgres']['host']
db_user = config_data['postgres']['user']
db_pass = config_data['postgres']['pass']
db_name = config_data['postgres']['db']
device = config_data['sensor']['type']
alias = config_data['sensor']['alias']
vendor = config_data['sensor']['vendor']
place = config_data['sensor']['location']
ip = config_data['sensor']['ip']
sensors = config_data['sensor']['sensors']

# get data from device
devurl = "http://" + ip + "/data.json"
with urllib.request.urlopen(devurl) as url:
    data = json.loads(url.read().decode())

# Initialize sensor values
pm10 = pm25 = temp = hpa = humidity = signal = None

# map data
for _data in data['sensordatavalues']:
    if _data['value_type'] == "SDS_P1":
        pm10 = float(_data['value'])
    if _data['value_type'] == "SDS_P2":
        pm25 = float(_data['value'])
    if _data['value_type'] == "BME280_temperature":
        temp = float(_data['value'])
    if _data['value_type'] == "BME280_pressure":
        hpa = float(_data['value'])
    if _data['value_type'] == "BME280_humidity":
        humidity = float(_data['value'])
    if _data['value_type'] == "signal":
        signal = int(_data['value'])

# print("pm10: {} pm25: {} temp: {} hum: {} hpa {} sig: {}".format(pm10, pm25, temp, humidity, hpa, signal))

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database=db_name
    )
except psycopg2.OperationalError as error:
    print(f"- error connecting to database: {error}")
    sys.exit(1)

cursor = conn.cursor()

# Insert data into PostgreSQL
sql = """
    INSERT INTO feinstaub_daten (
        timestamp, device, alias, vendor, sensors, location, pm10, pm2_5, temp, humidity, airpressure, sig
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
try:
    cursor.execute(sql, (dt, device, alias, vendor, str(sensors), place, pm10, pm25, temp, humidity, hpa, signal))
    conn.commit()
except psycopg2.Error as e:
    print(f"- error executing SQL: {e}")
    conn.rollback()

cursor.close()
conn.close()

