import sqlite3


con = sqlite3.connect("sqlite.db")
cur = con.cursor()

cur.execute("create table pedidos (id integer primary key autoincrement,username varchar(50),email varchar(50),description varchar(50))")