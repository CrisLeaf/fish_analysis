#%% Initial
import pandas as pd

disemb = pd.read_csv("data/disembarkation_year.csv")
fresh = pd.read_csv("data/fresh_production.csv")
frozen = pd.read_csv("data/frozen_production.csv")
prices = pd.read_csv("data/prices.csv")

def clean_price(value):
	value = value.replace("-", "0")
	value = value.replace(".", "")
	return int(value)

def clean_name(string):
	string = string.lower()
	string = string.replace("á", "a")
	string = string.replace("é", "e")
	string = string.replace("í", "i")
	string = string.replace("ó", "o")
	string = string.replace("ú", "u")
	string = string.replace("ñ", "n")
	return string

#%% Data Preprocess
prices.drop(index=[i for i in range(11)], inplace=True)
prices.drop(index=[12, 13], inplace=True)
prices.rename(columns={"Unnamed: 0": "ESPECIE", "ESPECIE 2001": "2001"}, inplace=True)

for index in range(1, disemb.shape[1]):
	disemb[disemb.columns[index]] = disemb[disemb.columns[index]].apply(lambda x: clean_price(x))

for index in range(1, fresh.shape[1]):
	fresh[fresh.columns[index]] = fresh[fresh.columns[index]].apply(lambda x: clean_price(x))

for index in range(1, frozen.shape[1]):
	frozen[frozen.columns[index]] = frozen[frozen.columns[index]].apply(lambda x: clean_price(x))

for index in range(1, prices.shape[1]):
	prices[prices.columns[index]] = prices[prices.columns[index]].apply(lambda x: clean_price(x))

disemb["ESPECIE"] = disemb["ESPECIE"].apply(lambda x: clean_name(x))
fresh["ESPECIE"] = fresh["ESPECIE"].apply(lambda x: clean_name(x))
frozen["ESPECIE"] = frozen["ESPECIE"].apply(lambda x: clean_name(x))
prices["ESPECIE"] = prices["ESPECIE"].apply(lambda x: clean_name(x))

acha = {"ESPECIE": "acha", "2001": 4343397, "2002": 4089638, "2003": 0, "2004": 4179266, "2005": 0,
		"2006": 385766, "2007": 4130245, "2008": 3793095, "2009": 4631032, "2010": 0,
		"2011": 3000000}

albacora = {"ESPECIE": "albacora", "2001": 4081583, "2002": 2796074, "2003": 4427918,
			"2004": 3701045, "2005": 3446078, "2006": 3832669, "2007": 3682982, "2008": 2634501,
			"2009": 2310613, "2010": 2822911, "2011": 2373333}

anchoveta = {"ESPECIE": "anchoveta", "2001": 104571, "2002": 73643, "2003": 102416, "2004": 80931,
			 "2005": 252660, "2006": 0, "2007": 67842, "2008": 59470, "2009": 88806, "2010": 0,
			 "2011": 82117}

anguila = {"ESPECIE": "anguila", "2001": 355105, "2002": 375029, "2003": 0, "2004": 352067,
		   "2005": 429921, "2006": 3184877, "2007": 350213, "2008": 511714, "2009": 0, "2010": 0,
		   "2011": 0}

apanado = {"ESPECIE": "apanado", "2001": 1362787, "2002": 1230324, "2003": 1102137, "2004": 1264749,
		   "2005": 1090790, "2006": 1453753, "2007": 1801786, "2008": 1927239, "2009": 1461103,
		   "2010": 1944863, "2011": 1257500}

prices = prices.append([acha, albacora, anchoveta, anguila, apanado], ignore_index=True)
prices.reset_index(drop=True, inplace=True)

#%% Data PSQL Names Insert
import psycopg2

unique_names = list(disemb["ESPECIE"].unique()) + list(fresh["ESPECIE"].unique()) + \
			   list(frozen["ESPECIE"].unique()) + list(prices["ESPECIE"].unique())
unique_names = set(unique_names)

host = "localhost"
user = "postgres"
password = "password"
dbname = "fishdb"

conn = psycopg2.connect(host=host, user=user, password=password, dbname=dbname)
curr = conn.cursor()

for name in unique_names:
	curr.execute(
		f"INSERT INTO fishes (name) VALUES ('{name}');"
	)
	
conn.commit()
curr.close()
conn.close()

#%% Data PSQL Values Insert
from itertools import product

conn = psycopg2.connect(host=host, user=user, password=password, dbname=dbname)
curr = conn.cursor()

for i, j in product(range(disemb.shape[0]), range(1, disemb.shape[1])):
	curr.execute(
		f"SELECT f_id FROM fishes WHERE name='{disemb.iloc[i, 0]}';"
	)
	f_id = curr.fetchall()[0][0]
	curr.execute(
		f"INSERT INTO disembarkation_year (year, value, f_id) "
		f"VALUES ('{disemb.columns[j]}', {disemb.iloc[i, j]}, {f_id});"
	)

for i, j in product(range(fresh.shape[0]), range(1, fresh.shape[1])):
	curr.execute(
		f"SELECT f_id FROM fishes WHERE name='{fresh.iloc[i, 0]}';"
	)
	f_id = curr.fetchall()[0][0]
	curr.execute(
		f"INSERT INTO production (year, value, state, f_id) "
		f"VALUES ('{fresh.columns[j]}', {fresh.iloc[i, j]}, 'fresh', {f_id});"
	)

for i, j in product(range(frozen.shape[0]), range(1, frozen.shape[1])):
	curr.execute(
		f"SELECT f_id FROM fishes WHERE name='{frozen.iloc[i, 0]}';"
	)
	f_id = curr.fetchall()[0][0]
	curr.execute(
		f"INSERT INTO production (year, value, state, f_id) "
		f"VALUES ('{frozen.columns[j]}', {frozen.iloc[i, j]}, 'frozen', {f_id});"
	)

for i, j in product(range(prices.shape[0]), range(1, prices.shape[1])):
	curr.execute(
		f"SELECT f_id FROM fishes WHERE name='{prices.iloc[i, 0]}';"
	)
	f_id = curr.fetchall()[0][0]
	curr.execute(
		f"INSERT INTO prices (year, value, f_id) "
		f"VALUES ('{prices.columns[j]}', {prices.iloc[i, j]}, {f_id});"
	)

conn.commit()
curr.close()
conn.close()