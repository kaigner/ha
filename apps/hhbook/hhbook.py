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

# Klassen Start

class Purchase():
	def __init__(self):
		self.date = None
		self.referencename = None
		self.ledger = {"id": None, "name": None} 
		self.store  = {"id": None, "name": None, "street": None, "housenumber": None} 

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

	def list(self, ask, id):
		try:
			with db.cursor() as cur:
					if id == 0:
							cur.execute("SELECT id, name, alias, street, housenumber,zip FROM store")
							rows = cur.fetchall()
					else:
							cur.execute("SELECT id, name, alias, street, housenumber,zip FROM store where id = %s", (id,))
							rows = cur.fetchall()
					printHeader()
					print("[green]Auswahl des Geschäftes:[/green]\n")
					for row in rows:
						print("{} -> {}  Alias: {}".format(row[0], row[1], row[2]))
		finally:
			cur.close()

			if ask == "yes":
					x = input("Enter für weiter")

	def choose(self):
		print("\n[magenta bold]Auswahl:[/magenta bold]", end="")
		x = input(" ")
		# simple Eingebaprüfung / SQL Injection Check - NACHARBEITEN
		try:
			val = int(x)
		except ValueError:
			print("Keine Zahl, Abbruch")
			sys.exit(1)

		try:
				with db.cursor() as cur:
						cur.execute("SELECT id, name, street, housenumber FROM store WHERE id = %s", (x,))
						row = cur.fetchone()
						purchase.store["id"] = int(row[0])
						purchase.store["name"] = row[1]
						purchase.store["street"] = row[2]
						purchase.store["housenumber"] = row[3]
		finally:
			cur.close()


class PackagingUnit():
	def __init__(self):
		self.pu_name = {"pu_id": None, "name": None, "shortname": None, "comment": None}

	def readFromDB(self):
		try:
			with db.cursor() as cur:
				cur.execute("select pu_id, name, shortname, comment from packagingunit")
				rows = cur.fetchall()
				for row in rows:
					print(row)
		finally:
			cur.close()




class Product():
	def __init__(self):
		self.product = {"name": None, "ean": None, "vendor": None, "packing": None, "packagingunit": None }

	def addProduct(self, name):
		console.clear()
		self.product["name"]          = input("Name des Produktes : ").strip()
		self.product["ean"]           = input("EAN                : ").strip()
		self.product["vendor"]        = input("Hersteller         : ").strip()
		self.product["packing"]       = input("Verpackung         : ").strip() #VERPAKUNGEN AUFLISTEN
		self.product["packagingunit"] = input("Verpackungs-Einheit: ").strip()
		try:
			with db.cursor() as cur:
				sql = "INSERT INTO product (name, ean, vendor, packing, packagingunit) VALUES (%s, %s, %s, %s, %s)"
				cursor.execute(sql,(self.product["name"], self.product["ean"], self.product["vendor"], self.product["packing"], self.product["packagingunit"]))
				db.commit()
		finally:
			cur.close()


		
		
		
		
		sys.exit(9)


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

				printHeader()
				print("[green]Auswahl des Geschäftes:[/green]\n")
				for row in rows:
					print("{} -> {}  Alias: {}".format(row[0], row[1], row[2]))	
		finally:
			cur.close()
		
		if ask == "yes":
			x = input("Enter für weiter")


	def choose(self):
		print("\n[magenta bold]Auswahl:[/magenta bold]", end="")
		x = input(" ")
		# simple Eingebaprüfung / SQL Injection Check - NACHARBEITEN 
		try: 
			val = int(x)
		except ValueError:
			print("Keine Zahl, Abbruch")
			sys.exit(1)
		
		try:
			with db.cursor() as cur:
				cur.execute("SELECT id, name, street, housenumber FROM store WHERE id = %s", (x,))
				row = cur.fetchone()
				purchase.store["id"] = int(row[0])
				purchase.store["name"] = row[1]
				purchase.store["street"] = row[2]
				purchase.store["housenumber"] = row[3]
		finally:
			cur.close()



class Ledger():
	def __init__(self):
		self.account = { "name":None, "iban":None }

	def readAll():
		try:
			with db.cursor() as cur:
				cur.execute("SELECT id, name, comment, iban FROM ledger")
				rows = cur.fetchall()
		finally:
			cur.close()
	
	def list(self, ask, id):
			try:
				with db.cursor() as cur:
					if id == 0:
						cur.execute("SELECT id, name, comment, iban FROM ledger")
						rows = cur.fetchall()
					else:
						cur.execute("SELECT id, name, comment, iban FROM ledger where id = %s", (id,))
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


class Packaging():
	def __init__(self):
		self.quantity = {}
	
	def read(self):
		try:
			with db.cursor() as cur:
				cur.execute("select pa_id, name from packaging")
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


# def addProducttoDB(name, store, ledger, pruchasedate, scanname):
# 	print("Name: {}".format(name))
# 	print("EAN", end="")
# 	ean = input(": ").strip()
# 	print("Hersteller", end="")
# 	manufactor = input(": ").strip()
# 	print("Verpackung", end="")
# 	packaging = input(": ").strip()
# 	print("Verpackungseinheit", end="")
# 	quant.list()
# 	packagingunit = input(": ")
# 	try:
# 		with db.cursor() as cur:
# 			sql = "INSERT INTO product (name, ean, vendor, packing, packagingunit) VALUES (%s, %s, %s, %s, %s)"
# 			cur.execute(sql,(name, ean, manufactor, packaging, packagingunit ))
# 			db.commit()

# 	finally:
# 		cur.close()
# 	# searchArticel(name , store, ledger, pruchasedate, scanname)

def addProduct(name):
	printHeader()
	print("Name {}".format(name), end="")
	t_name = input(": ").strip()
	if t_name != "":
		name = t_name
	print("EAN", end="")
	ean = input(": ").strip()
	print("Hersteller", end="")
	manufactor = input(": ").strip()
	
	print("Verpackung", end="")
	
	
	
	
	packaging = input(": ").strip()
	
	
	print("Verpackungseinheit", end="")
	quant.list()
	packagingunit = input(": ")


def searchProduct(name):
	try:
		with db.cursor() as cur:
			# Suche Produkt in Produkt DB
			# cur.execute("select id, item, price from purchase where item like %s", (name,))
			cur.execute("SELECT product_id, name, ean, vendor, packing, packagingunit FROM product where name like %s", (name,))
			rows = cur.fetchall()
			if len(rows) == 0:
				print("Kein Produkt gefunden! - neu anlegen oder neue suche? (default neu, derzeit einzige option")
				x = input("Enter um Produkt anzulegen")
				product.addProduct(name)

			else:
				print("gefundene Produkte:")
				for row in rows:
					print(row)
				return True


			# Neustart mit dem Ergebnis
			print("ende")
			sys.exit(1)
	finally:
		cur.close()


def addPurchaseToDB(pruchasedate, scanname, store, ledger, name, stueck, kprostueck, price, menge, mengeneinheit, kategorie):
	try:
		with db.cursor() as cur:
			sql = "INSERT INTO purchase (timestamp, receipt, store, ledger, name, quantity, quantityprice, price, unitofquantityprice, category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			cursor.execute(sql, \
				( \
					pruchasedate, \
					scanname, \
					store, \
					ledger, \
					name, \
					stueck, \
					kprostueck, \
					price, \
					mengeneinheit,\
					kategorie \
					))
			db.commit()
	finally:
		cur.close()


def askDate():	# Datum
	while True:
		try:
			# dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			print("Einkaufsdatum ({})".format(dt), end="")
			purchasedate = input(": ").strip()
			if purchasedate == "":
				purchasedate = dt
			datetime.strptime(purchasedate, '%Y-%m-%d %H:%M:%S')
		except ValueError:
			continue
		else:
			purchase.date = purchasedate
			break

	
def add_purchase():
	dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	
	# Kontowahl
	nl.list("n",0)
	nl.choose()
	printHeader()
	
	# Wahl des Geschäftes
	ns.list("n", 0)
	ns.choose()
	printHeader()


    # Nach Datum Fragen
	askDate()
	printHeader()
	
	# Beleg
	print("Dateiname des Belegs", end="")
	purchase.referencename = input(": ")
	printHeader()
	
	
	# ###################
	# Eingabe der Artikel
	# ###################
	# 
	# 		
	print('Artikel eingeben ("ende" als Artikelname für Eingabeende')
	
	while True:
		name = input("Artikel: ")
		if name == "ende":
			break
		# Artikel schon in der Datenbank?
		searchProduct(name)
		

		
		
		
		# ALT searchArticel(name, store, ledger, pruchasedate, scanname)

	
	
	
	
	
	
	
	x = input("Einkauf Ende")

def printHeader():
	console.clear() 
	print("[yellow underline]\nHaushaltsbuch v0.0.1a[/yellow underline]")
	print("\n")
	if purchase.ledger["name"] is None:
		print("Konto    : - leer -")
	else:
		print("Konto    : [sky_blue2]{}[/sky_blue2]".format(purchase.ledger["name"]))

	if purchase.store["name"] is None:
		print("Geschäft : - leer -")
	else:
		print("Geschäft : [sky_blue2]{} {} {}[/sky_blue2]".format(purchase.store["name"], purchase.store["street"], purchase.store["housenumber"]))
	
	if purchase.date is None:
		print("Datum    : - leer -")
	else:
		print("Datum    : {}".format(str(purchase.date)))

	if purchase.referencename is None:
		print("Belegname: - leer -")
	else:
		print("Belegname: {}".format(purchase.referencename))
	
	print("\n----------------------------------------------------------\n")

	
	
	
	
	# print("(Konto: {} - Geschäft: {})".format(purchase.ledger, purchase.store))
	print("\n\n")


if __name__ == "__main__":
	console = Console()
	cat = Categorys()
	cat.read()
	product = Product()
	quant = Packaging()
	quant.read()
	purchase = Purchase()
	nl = Ledger()
	ns = Store()

	pu = PackagingUnit()
	pu.readFromDB()
	sys.exit

	

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

