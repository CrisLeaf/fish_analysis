import psycopg2

host = "localhost"
user = "postgres"
password = "password"
dbname = "fishdb"

conn = psycopg2.connect(host=host, user=user, password=password, dbname=dbname)
curr = conn.cursor()

curr.execute(
	"CREATE TABLE fishes (f_id SERIAL PRIMARY KEY, name VARCHAR(250) UNIQUE NOT NULL);"
)
curr.execute(
	"CREATE TABLE disembarkation_year (dy_id SERIAL PRIMARY KEY, year VARCHAR(100) NOT NULL, "
	"value INT, f_id INT NOT NULL, FOREIGN KEY (f_id) REFERENCES fishes (f_id));"
)
curr.execute(
	"CREATE TABLE production (p_id SERIAL PRIMARY KEY, f_id INT NOT NULL, "
	"year VARCHAR(100) NOT NULL, state VARCHAR(100), value INT, "
	"FOREIGN KEY (f_id) REFERENCES fishes (f_id));"
)
curr.execute(
	"CREATE TABLE prices (pr_id SERIAL PRIMARY KEY, f_id INT NOT NULL, "
	"year VARCHAR(100) NOT NULL, "
	"value INT, FOREIGN KEY (f_id) REFERENCES fishes (f_id));"
)

conn.commit()
curr.close()
conn.close()