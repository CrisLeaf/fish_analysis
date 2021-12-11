import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")
import streamlit as st
import psycopg2

#%% Connect to PSQL
host = "localhost"
user = "postgres"
password = "password"
dbname = "fishdb"

#%% Back-End
def get_statistics(name):
	name = name.lower()
	# PSQL Connection
	conn = psycopg2.connect(host=host, user=user, password=password, dbname=dbname)
	curr = conn.cursor()
	curr.execute(
		f"SELECT * FROM fishes WHERE name='{name}';"
	)
	f_id = curr.fetchall()[0][0]
	
	curr.execute(
		f"SELECT * FROM disembarkation_year WHERE f_id={f_id};"
	)
	items = curr.fetchall()
	disemb_years = [item[1] for item in items]
	disemb_values = [item[2] for item in items]
	
	curr.execute(
		f"SELECT * FROM production WHERE f_id={f_id};"
	)
	items = curr.fetchall()
	production_years = [item[2] for item in items]
	production_values = [item[4] for item in items]
	production_state = [item[3] for item in items]
	production_state = [
		"Fresco" if string == "fresh" else "Congelado" for string in production_state
	]
	curr.execute(
		f"SELECT * FROM prices WHERE f_id={f_id};"
	)
	items = curr.fetchall()
	prices_years = [item[2] for item in items]
	prices_values = [item[3] for item in items]
	conn.commit()
	curr.close()
	conn.close()
	# Plots
	fig, axes = plt.subplots(nrows=3, figsize=(10, 30))
	# disembarkation_year plot
	sns.lineplot(disemb_years, disemb_values, ax=axes[0])
	axes[0].set_title(f"Desembarque de {name[0].upper() + name[1:]} por año", fontsize=15)
	axes[0].set_ylabel("Toneladas", fontsize=12)
	axes[0].set_xlabel("Año", fontsize=12)
	# production plot
	sns.lineplot(production_years, production_values, hue=production_state, ax=axes[1])
	axes[1].set_title(f"Producción de {name[0].upper() + name[1:]} por año", fontsize=15)
	axes[1].set_ylabel("Toneladas", fontsize=12)
	axes[1].set_xlabel("Año", fontsize=12)
	# prices plot
	sns.lineplot(prices_years, prices_values, ax=axes[2])
	axes[2].set_title(f"Precios de {name[0].upper() + name[1:]} por año", fontsize=15)
	axes[2].set_ylabel("Precio por tonelada", fontsize=12)
	axes[2].set_xlabel("Año", fontsize=12)
	plt.show()
	
	return fig, prices_values
	
#%% Front-End
def main():
	# Page
	html_temp="""
	<h1 style="color:#ffffff;text-align:center;">Estadísticas de Pesca</h1>
	</div>
	"""
	# Data
	st.markdown(html_temp, unsafe_allow_html=True)
	name = st.text_input("Nombre")
	# Button
	if st.button("Obtener Estadísticas:"):
		try:
			fig, prices = get_statistics(name)
			st.pyplot(fig)
			mean = int(np.mean(prices) + 0.5)
			mean = f"{mean:,}".replace(",", ".")
			st.success(f"Media de precios: {mean}")
			std = int(np.std(prices) + 0.5)
			std = f"{std:,}".replace(",", ".")
			st.success(f"Desviación de precios: {std}")
		except:
			st.success(f"{name} no se encuentra en la base de datos.")

if __name__ == "__main__":
	main()