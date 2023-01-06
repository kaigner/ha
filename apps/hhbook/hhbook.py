#!/usr/bin/python3.8

# import curses
# from curses import wrapper
from rich import print
from rich.console import Console
import os
import json
import pymysql
import sys
from datetime import datetime



# Lese Konfig 
os.chdir(os.path.dirname(__file__))

# Read Config File
with open(os.getcwd() + "/config.json") as json_config_file:
	config_data=json.load(json_config_file)
db_host = config_data['mysql']['host']
db_user = config_data['mysql']['user']
db_pass = config_data['mysql']['pass']
db_name = config_data['mysql']['db']

dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Connect to Database
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

# sql = "INSERT INTO paxdata (wifi, ble, gwname, gweui, freq, dt, location) VALUES (%s, %s, %s, %s, %s, %s, %s)"
# cursor.execute(sql,(wifi, ble, gwname, gweui, freq, dt, location))


def hhbook_exit():
	db.close()
	sys.exit(1)



def list_stores():
	print("list_stores")

def add_newstore():
	print("add_newstore")

if __name__ == "__main__":
	console = Console()
	while True:
		console.clear()		
		print("[yellow underline]\nHaushaltsbuch v0.0.1a[/yellow underline]")
		print("\n\n")
		print("neuer einkauf")
		print("einlauf anzeigen")
		print("\n\n\n")
		print("1, neues Geschäft anlegen")
		print("\n\n")
		print("x, Beenden")

		x = input("Auswahl: ").strip()

		print("\nEingabe: {}".format(x))

		if x == "x":
			hhbook_exit()
		elif x == 1:
			add_newstore()
		else:
			pass
	
