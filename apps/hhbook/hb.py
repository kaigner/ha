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
    sys.exit(1)

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
        self.store = {"id": None, "name": None,
                      "street": None, "housenumber": None}


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
        try:
            with db.cursor() as cur:
                cur.execute("SELECT id, name, comment, iban FROM ledger")
                rows = cur.fetchall()
        finally:
            cur.close()
        for row in rows:
            print("Idx:{} -> {}".format(row[0], row[1]))

        print("\n[magenta bold]Auswahl:[/magenta bold]", end="")
        x = get_number_input(0, int(len(rows)))
        try:
            with db.cursor() as cur:
                cur.execute("SELECT id, name FROM ledger WHERE id = %s", (x,))
                row = cur.fetchone()
                purchase.ledger["id"] = int(row[0])
                purchase.ledger["name"] = row[1]
        finally:
            pass



def get_number_input(n, x):
    while True:
        user_input = input()
        if user_input.isdigit():
            number = int(user_input)
            if n <= number <= x:
                return number
            else:
                print("Bitte geben Sie eine Zahl zwischen {} und {} ein: ".format(n, x))
        else:
            print("Bitte geben Sie eine Zahl zwischen {} und {} ein: ".format(n, x))


def hb_exit():
    db.close()
    sys.exit(1)


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

    while True:
        # console.clear()
        # print("[yellow underline]\nHaushaltsbuch v0.0.1a[/yellow underline]")
        # print("\n\n")
        printHeader()
        print("[blue][bold]n[/bold], neuer Einkauf[/blue]")
        print("einlauf anzeigen")
        print("\n\n\n")
        print("1, neues Geschäft anlegen")
        print("2, Geschäfte anzeigen")
        print("\n----------------------\n")
        print("3, neues Konto anlegen")
        print("4, Konto Auswählen")
        print("\n\n")
        print("x, Beenden")

        x = input("Auswahl: ").strip()

        print("\nEingabe: {}".format(x))

        if x == "x":
            hb_exit()
        elif x == "n":
            add_purchase()
        elif x == "1":
            add_newstore()
        elif x == "2":
            list_stores()
        elif x == "4":
            bank_account.choose()
        else:
            pass
        # x = input("neuer lauf")
