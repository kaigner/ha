#!/usr/bin/env python3
#from __future__ import print_function # use print function syntax from python3.x
import time
#import datetime
from datetime import datetime
import paho.mqtt.client as mqtt
#import psycopg2
import pymysql
import json
import http.client, urllib, sys



def on_message(client, userdata, message):
    msg=str(message.payload.decode("utf-8"))
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #print("on message: "+msg)
    if msg == "offen":
        #print("if offen")
        if datetime.today().weekday() == 1:
            print("Pushover Dummy")
            # print("Sende Pushover Nachricht")
            # send_po("Wohnungstuer Türöffnung erkannt")
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - Wohnungstür wurde geöffnet")
        cur.execute("INSERT INTO lock_status (timestamp, name, is_locked, comment) VALUES (%s, %s, %s, %s)", (dt, "WohnungsTür", 0, ""))
    elif msg == "geschlossen":
        
        cur.execute("INSERT INTO lock_status (timestamp, name, is_locked, comment) VALUES (%s, %s, %s, %s)", (dt, "WohnungsTür", 1, ""))
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - Wohnungstür wurde geschlossen")
    else:
        print("unbekannte Nachricht: "+msg)
    conn.commit()

def send_po(po_msg):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.parse.urlencode({
      "token": "aoes6389k16yavmwd1bigjz8kmn3ax",
      "user": "g6y7wphkbi763nqqt99rza1zujx2ip",
      "message": ""+po_msg+"",
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

filepath="/tmp/"
broker_address="192.168.2.2"
client = mqtt.Client("c2")
client.connect(broker_address)
client.subscribe("smarthome/Wohnungstuer/lock_status")
client.on_message=on_message

# Read Config File
with open("lock_status.cfg") as json_config_file:
        config_data=json.load(json_config_file)
db_host = config_data['mysql']['host']
db_user = config_data['mysql']['user']
db_pass = config_data['mysql']['pass']
db_name = config_data['mysql']['db']
db_port = config_data['mysql']['port']


# Open connection to DB
conn = pymysql.connect(database=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
cur = conn.cursor()

while True:
    client.loop_start()
    time.sleep(60)
    client.loop_stop()
