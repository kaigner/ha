#!/usr/bin/env python

import time
from datetime import datetime
import psycopg2
import json

import urllib.request
import json
import psycopg2

dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
device = "NODEMCUV3_SDS011"
alias  = "feinstaub"
vendor = "DIY - luftdaten.info"
place  = "Dachauer Str217"

# Read Config File
with open("/home/klaus/GIT/ha/scripts/config.json") as json_config_file:
        config_data=json.load(json_config_file)
db_host = config_data['postgres']['host']
db_user = config_data['postgres']['user']
db_name = config_data['postgres']['db']


conn = psycopg2.connect(dbname=db_name, user=db_user, host=db_host, port="5433")
cur = conn.cursor()


with urllib.request.urlopen("http://192.168.2.5/data.json") as url:
       data = json.loads(url.read().decode())


# print(json.dumps(data, indent=4, sort_keys=True))

pm10   = (data["sensordatavalues"][0]["value"])
pm25   = (data['sensordatavalues'][1]['value'])
temp   = (data['sensordatavalues'][2]['value'])
hpa    = (data['sensordatavalues'][3]['value'])
hum    = (data['sensordatavalues'][4]['value'])
signal = (data['sensordatavalues'][-1]['value'])
# print("pm10: {} pm25: {} temp: {} hum: {} hpa {} sig: {}".format(pm10, pm25, temp, hum, hpa, signal))


cur.execute("INSERT INTO feinstaub_sensor (timestamp, device, alias, vendor, place, pm10, pm25, temp, humidity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (dt, device, alias, vendor, place, pm10, pm25, temp, hum))
conn.commit()
conn.close()

