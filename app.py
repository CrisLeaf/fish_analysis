#%% Connect to PSQL
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as sl
import psycopg2

host = "localhost"
user = "postgres"
password = "password"
dbname = "fishdb"

#%%
conn = psycopg2.connect(host=host, user=user, password=password, dbname=dbname)
curr = conn.cursor()

curr.execute(
	f"SELECT * FROM fishes WHERE name='bonito';"
)
f_id = curr.fetchall()[0][0]
print(f"albacora id: {f_id}")

curr.execute(
	f"SELECT * FROM prices WHERE f_id={f_id};"
	# "DELETE FROM fishes *;"
)

print(curr.fetchall())

conn.commit()
curr.close()
conn.close()


#%%

def main():
	# Page
	html_temp="""
	<h1 style="color:#181082;text-align:center;">Linear Model</h1>
	</div>
	"""
	# Data
	sl.markdown(html_temp, unsafe_allow_html=True)
	x1 = sl.text_input("X1")
	x2 = sl.text_input("X2")
	# Button
	if sl.button("Enter:"):
		x_in = [np.float_(x1.title()),
				np.float_(x2.title())]
		predicts = model_prediction(x_in, model)
		sl.success(f": {predicts}")


if __name__ == "__main__":
	main()