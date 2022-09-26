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
device = "NODEMCUV3_SDS011"
alias  = "feinstaub"
vendor = "DIY - luftdaten.info"
place  = "Dachauer Str217"


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


os.chdir(os.path.dirname(__file__))

# Create custom logger logging all five levels
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Define format for logs
fmt = '%(asctime)s | %(levelname)8s | %(message)s'

# Create stdout handler for logging to the console (logs all five levels)
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(CustomFormatter(fmt))


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


# get data from device
devurl = "http://" + ip + "/data.json"
with urllib.request.urlopen(devurl) as url:
       data = json.loads(url.read().decode())

# map data
for _data in data['sensordatavalues']:
    #print(_data)
    #print("{} :  {}".format(_data['value_type'],  _data['value']))
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

# +-------------+--------------+------+-----+---------------------+-------------------------------+
# | Field       | Type         | Null | Key | Default             | Extra                         |
# +-------------+--------------+------+-----+---------------------+-------------------------------+
# | timestamp   | timestamp    | NO   |     | current_timestamp() | on update current_timestamp() |
# | device      | varchar(255) | YES  |     | NULL                |                               |
# | alias       | varchar(255) | YES  |     | NULL                |                               |
# | vendor      | varchar(255) | YES  |     | NULL                |                               |
# | sensor1     | varchar(255) | YES  |     | NULL                |                               |
# | sensor2     | varchar(255) | YES  |     | NULL                |                               |
# | location    | varchar(255) | YES  |     | NULL                |                               |
# | pm10        | float        | YES  |     | NULL                |                               |
# | pm2_5       | float        | YES  |     | NULL                |                               |
# | temp        | float        | YES  |     | NULL                |                               |
# | humidity    | float        | YES  |     | NULL                |                               |
# | airpressure | float        | YES  |     | NULL                |                               |
# | json_data   | varchar(255) | YES  |     | NULL                |                               |
# +-------------+--------------+------+-----+---------------------+-------------------------------+



print("pm10: {} pm25: {} temp: {} hum: {} hpa {} sig: {}".format(pm10, pm25, temp, humidity, hpa, signal))

try:
	db = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
except pymysql.err.OperationalError as error:
	print("- error connecting to database: {}".format(error))
	sys.exit(1)
cursor = db.cursor()
if (db):
    logger.info("Datenbankverbindung OK")
else:
    logger.critical("Datenbankversbingung FEHLER")
    sys.exit(0)

        # sql = "INSERT INTO common_data (device, type, event, reading, json_data, unit) VALUES (%s, %s, %s, %s, %s, %s)"
        # cursor.execute(sql,(dev, dev_type, "update", "data", json.dumps(self.data), "json" ))
        # db.commit()
db.close()
logger.info("db INSERT\n====================")
sys.exit(0)


cur.execute("INSERT INTO feinstaub_sensor (timestamp, device, alias, vendor, place, pm10, pm25, temp, humidity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (dt, device, alias, vendor, place, pm10, pm25, temp, hum))
conn.commit()
conn.close()

