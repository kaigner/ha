#!/usr/bin/env python3

from datetime import datetime
import time
import json
import pymysql
from requests.auth import HTTPBasicAuth
import requests
import os
import sys



# Lese Konfig 
os.chdir(os.path.dirname(__file__))

# Read Config File
with open(os.getcwd() + "/config.json") as json_config_file:
        config_data=json.load(json_config_file)
shelly_user  = config_data['http_auth']['user']
shelly_pass  = config_data['http_auth']['pass']
db_host  = config_data['mysql']['host']
db_user  = config_data['mysql']['user']
db_pass  = config_data['mysql']['pass']
db_name  = config_data['mysql']['db']


shellys = {"192.168.2.21":"shelly_plug_s_spuelmaschine", "192.168.2.22":"shelly_plug_s_ap_klaus", "192.168.2.23":"shelly_plug_s_ap_claudia", "192.168.2.24":"shelly_plug_s_bad"}


def get_status_in_json(ipaddr):
    try:
        response = requests.get('http://' + ipaddr + '/status', auth=HTTPBasicAuth(shelly_user, shelly_pass))
        return(response.json())
    except:
        print("Kann shelly mit der ip: {} nicht erreichen".format(ipaddr))


def insert_json_data_to_database(json_data, aliasname):
    device = json_data["mac"]
    vendor = "Shelly"
    try:
        db = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
        cursor = db.cursor()
        sql = "INSERT INTO common_data (timestamp, device, type, json_data, unit) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (dt, aliasname, vendor, json.dumps(json_data), "json"))
        db.commit()
        db.close()
        cursor.close
    except pymysql.err.OperationalError as error:
        print("- error connecting to database: {}".format(error))
        # sys.exit(1)


def parse_json_and_do_the_rest_because_i_have_no_class(json_data):
    print(json_data["mac"])


if __name__ == "__main__":
    while True: 
        print("Konfigurierte Shellys:")
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for key, value in shellys.items():
            ipaddr    = key
            aliasname = value
            json_data = get_status_in_json(ipaddr)
            if json_data is not None:
                parse_json_and_do_the_rest_because_i_have_no_class(json_data)
                insert_json_data_to_database(json_data, aliasname)
            json_data = {}
        time.sleep(60)


sys.exit(0)





