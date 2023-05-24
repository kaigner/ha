#!/usr/bin/env python3

from datetime import datetime
import json
import pymysql
import pytz
import os
from rich import print
from rich.console import Console
import sys


# Lese Konfig
os.chdir(os.path.dirname(__file__))

# Read Config File
with open(os.getcwd() + "/config.json") as json_config_file:
    config_data = json.load(json_config_file)
db_host = config_data['mysql']['host']
db_user = config_data['mysql']['user']
db_pass = config_data['mysql']['pass']
db_name = config_data['mysql']['db']

dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Connect to Database
try:
    db = pymysql.connect(host=db_host, user=db_user, password=db_pass,
                         database=db_name)
except pymysql.err.OperationalError as error:
    print("- error connecting to database: {}".format(error))
    pass

cursor = db.cursor()
if (db):
    print("Datenbankverbindung OK")
    # pass #print("Datenbankverbindung OK")
else:
    print("konnte keine Verbindung zur Datenbank herstellen")
    sys.exit(9)


class receipt:
    def __init__(self):
        self.date = datetime.now(pytz.timezone('Europe/Berlin'))
        self.purchase_nr = 0
        self.store = 0
        self.article = ""
        self.single_price = 0
        self.amount = 0
        self.total_price = 0
        self.single_weight = 0
        self.total_weight = 0
        self.store_flag_0 = ""
        self.my_category = ""


class Store():
    def __init__(self):
        self.id = 0
        self.name = ""
        self.alias = ""
        self.street = ""
        self.housenumber = ""
        self.zip = 0
        self.town = ""
        self.state = "Bayern"
        self.country = "Deutschland"

class Purchase():
	def __init__(self):
		self.date = None
		self.referencename = None
		self.ledger = {"id": None, "name": None} 
		self.store  = {"id": None, "name": None, "street": None, "housenumber": None} 

class Ledger():
    def __init__(self):
        self.account = {"name": None, "iban": None}

    def readAll():
        print("start l.readAll")
        try:
            with db.cursor() as cur:
                cur.execute("SELECT id, name, comment, iban FROM ledger")
                rows = cur.fetchall()
        finally:
            cur.close()

    def xlist(self, ask, id):
        try:
            with db.cursor() as cur:
                if id == 0:
                    cur.execute("SELECT id, name, comment, iban FROM ledger")
                    rows = cur.fetchall()
                else:
                    cur.execute(
                        "SELECT id, name, comment, iban FROM ledger where id = %s", (id,))
                    rows = cur.fetchall()

                printHeader()
                print("[green]Konto Auswahl:[/green]\n")
                for row in rows:
                    print("{} -> {}".format(row[0], row[1]))
        finally:
            cur.close()

        if ask == "yes":
            x = input("Enter für weiter")

    def choose(self):
        print("\n[magenta bold]Auswahl:[/magenta bold]", end="")
        x = input(" ")
        if x == "":
            x = 1
        # simple Eingebaprüfung / SQL Injection Check - NACHARBEITEN
        try:
            val = int(x)
        except ValueError:
            print("Keine Zahl, Abbruch")
            sys.exit(1)

        try:
            with db.cursor() as cur:
                cur.execute("SELECT id, name FROM ledger WHERE id = %s", (x,))
                row = cur.fetchone()
                purchase.ledger["id"] = int(row[0])
                purchase.ledger["name"] = row[1]
        finally:
            cur.close()


def printHeader():
    console.clear()
    print("[yellow underline]\nHaushaltsbuch v0.0.1a[/yellow underline]")
    print("\n")
    if purchase.ledger["name"] is None:
        print("Konto    : - leer -")
    else:
        print(
            "Konto    : [sky_blue2]{}[/sky_blue2]".format(purchase.ledger["name"]))

    if purchase.store["name"] is None:
        print("Geschäft : - leer -")
    else:
        print("Geschäft : [sky_blue2]{} {} {}[/sky_blue2]".format(
            purchase.store["name"], purchase.store["street"], purchase.store["housenumber"]))

    if purchase.date is None:
        print("Datum    : - leer -")
    else:
        print("Datum    : {}".format(str(purchase.date)))

    if purchase.referencename is None:
        print("Belegname: - leer -")
    else:
        print("Belegname: {}".format(purchase.referencename))

    print("\n----------------------------------------------------------\n")



if __name__ == "__main__":
    console = Console()
    bank_account = Ledger()
    purchase = Purchase()
    printHeader()






