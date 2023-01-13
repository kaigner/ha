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

class Store():
	def __init__(self):
		self.store = { "name":None, "alias":None, "street":None, "housenumber":None, "zip":None, "town":None, "state":None, "country":None}

	def askforData(self):
		console.clear() 
		self.store['name'] = input("Name des Geschäfts: ").strip()
		self.store['alias'] = input("Aliasname         : ").strip()
		self.store['street'] = input("Strasse           : ").strip()
		self.store['housenumber'] = input("Hausnummer        : ").strip()
		self.store['zip'] = input("PLZ               : ").strip()
		self.store['town'] = input("Stadt             : ").strip()
		self.store['state'] = input("State/Bezirk      : ").strip()
		self.store['country'] = input("Land              : ").strip()
		print("\n")
		while True:
			x = input("Daten Ok(ja/nein)?: ").strip()
			if x == "ja":
				return "yes"
			elif x == "nein":
				return "rerun"
			else:
				print('Bitte "ja" oder "nein" eingeben, Danke! :)', ":nerd_face:")

	def addtoDB(self):
		print("Add Store to DB")
		dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		sql = "INSERT INTO store (name, alias, street, housenumber, zip, town, state, country, created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
		cursor.execute(sql,(self.store["name"], self.store["alias"], self.store["street"], self.store["housenumber"], self.store["zip"], self.store["town"], self.store["state"], self.store["country"], dt))
		db.commit()
		cursor.close
		print("\n\n[italic green]Geschädt angelegt[/italic green]")

	def list(self, ask, id):
		try:
			with db.cursor() as cur:
				if id == 0:
					cur.execute("SELECT id, name, alias, street, housenumber,zip FROM store")
					rows = cur.fetchall()
				else:
					cur.execute("SELECT id, name, alias, street, housenumber,zip FROM store where id = %s", (id,))
					rows = cur.fetchall()

				for row in rows:
					print(row)	
		finally:
			cur.close()
		
		if ask == "yes":
			x = input("Enter für weiter")

	def choise(self):
		print("")
		x = input("Geschäft wählen: ")
		return x


class Ledger():
	def __init__(self):
		self.account = { "name":None, "iban":None }
	
	def list(self, ask):
		try:
			with db.cursor() as cur:
				cur.execute("SELECT id, name, comment FROM ledger")
				rows = cur.fetchall()
				for row in rows:
					print(row)
		finally:
			cur.close()
		if ask == "y":
			x = input("Enter für weiter")

	def list(self, ask, id):
			try:
				with db.cursor() as cur:
					if id == 0:
						cur.execute("SELECT id, name, comment, iban FROM ledger")
						rows = cur.fetchall()
					else:
						cur.execute("SELECT id, name, comment, iban FROM ledger where id = %s", (id,))
						rows = cur.fetchall()
			
					for row in rows:
						print(row)	
			finally:
				cur.close()
			
			if ask == "yes":
				x = input("Enter für weiter")


	def choose(self):
		print("")
		x = input("konto wählen: ")
		return x


class Categorys():
	def __init__(self):
		self.category = {}
	
	def read(self):
		try:
			with db.cursor() as cur:
				cur.execute("select id, name from categorys")
				rows = cur.fetchall()
				for id, name in rows:
					self.category[id]=name
		finally:
			cur.close()
		
	def list(self):
		for id, name in self.category.items():
			print("Id: {}  Name: {}".format(id, name))


class Quantitiys():
	def __init__(self):
		self.quantity = {}
	
	def read(self):
		try:
			with db.cursor() as cur:
				cur.execute("select id, name from quantitys")
				rows = cur.fetchall()
				for id, name in rows:
					self.quantity[id]=name
		finally:
			cur.close()
		
	def list(self):
		for id, name in self.quantity.items():
			print("Id: {}  Name: {}".format(id, name))
# Klassen ENDE



def hhbook_exit():
	db.close()
	sys.exit(1)
 

def list_stores():
	print("list_stores")
	ls = Store()
	ls.list("yes",0)


def add_newstore():
	print("add_newstore")
	ns = Store()
	rc = ns.askforData()
	if rc == "rerun":
		add_newstore()
	elif rc == "yes":
		print("add to db")
		ns.addtoDB()

def searchArticel(name, store):
	print("searchArticel")
	try:
		with db.cursor() as cur:
			cur.execute("select id, item, price from purchase where item like %s", (name,))
			rows = cur.fetchall()
			if len(rows) == 0:
				print("Keine bisherigen Einträge gefunden, Artikel wird neu eingetragen")
				while True:
					print("Stück            ", end="")
					stueck = input(": ")
					print("Kosten pro Stueck", end="")
					kprostueck = input(": ").replace(",",".")
					if kprostueck != "":
						price = float(kprostueck) * float(stueck)
						print("Kostet       : {}".format(str(price)))
					else:
						print("Kostet       ", end="")
						price = input(": ")
					
					print("Menge (Inhalt)   ", end="")
					menge = input(": ")
					quant.list()
					print("Mengen-Einheit   ", end="")
					mengeneinheit = input(": ")
					cat.list()
					print("Kategorie        ", end="")
					kategorie = input(": ")
					addPurchaseToDB(store, name, stueck, kprostueck, price, menge, mengeneinheit, kategorie)

					break
			else:
				print("such ergebniss:")
				for row in rows:
					print(row)
	finally:
		cur.close()



def addPurchaseToDB(store, name, stueck, kprostueck, price, menge, mengeneinheit, kategorie):
	print("Adde")



def add_purchase():
	print("add purchase")
	nl = Ledger()
	ns = Store()
	dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	nl.list("n",0)
	ledger = nl.choose()
	print("Konto Nr: {}".format(ledger))

	ns.list("n", 0)
	store = ns.choise()
	print("Store: {}".format(store))
	console.clear()
	print("[yellow underline]\nHaushaltsbuch v0.0.1a[/yellow underline]")
	print("\n\n")
	print("Ausgewähltes Konto: ")
	nl.list("no", ledger)
	# print("\n")
	print("Ausgewählter Laden:")
	ns.list("no", store)
	print("Einkaufsdatum ({})".format(dt), end="")
	pruchasedate = input(": ").strip()
	if pruchasedate == "":
		pruchasedate = dt
	# Prüfung ob es ein Dagum ist das in die Datenbank passt
	print("Dateiname des Belegs", end="")
	scanname = input(": ")
	print("artikel eingeben (ende als Artikelname für Eingabeende")
	while True:
		name = input("Artikel: ")
		if name == "ende":
			break
		searchArticel(name, store)


	
	





	

	

	x = input("Einkauf Ende")


if __name__ == "__main__":
	console = Console()
	cat = Categorys()
	quant = Quantitiys()
	cat.read()
	quant.read()
	

	while True:
		console.clear() 
		print("[yellow underline]\nHaushaltsbuch v0.0.1a[/yellow underline]")
		print("\n\n")
		print("[blue][bold]n[/bold], neuer Einkauf[/blue]")
		print("einlauf anzeigen")
		print("\n\n\n")
		print("1, neues Geschäft anlegen")
		print("2, Geschäfte anzeigen")
		print("\n----------------------\n")
		print("3, neues Konto anlegen")
		print("4, Konten auflisten")
		print("\n\n")
		print("x, Beenden")

		x = input("Auswahl: ").strip()

		print("\nEingabe: {}".format(x))

		if x == "x":
			hhbook_exit()
		elif x == "n":
			add_purchase()
		elif x == "1":
			add_newstore()
		elif x == "2":
			list_stores()
		else:
			pass
		# x = input("neuer lauf")

