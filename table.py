import sqlite3


conn = sqlite3.connect("classif.sqlite")
cursor = conn.cursor()
sql_query = """ CREATE TABLE client (
    id integer PRIMARY KEY AUTOINCREMENT,
    classe text NOT NULL,
    travel text NOT NULL,
    age integer NOT NULL,
    sexe text NOT NULL,
    baggage integer NOT NULL,
    time integer NOT NULL,
    gate integer NOT NULL,
    seat integer NOT NULL,
    intertainment integer NOT NULL,
    food integer NOT NULL,
    wifi integer NOT NULL,
    booking integer NOT NULL,
    service integer NOT NULL,
    commentaire text NOT NULL,
    satisfaction text NOT NULL
)"""
cursor.execute(sql_query)
sql = """ CREATE TABLE Admin (
    id integer PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL,
    password text NOT NULL
)"""
cursor.execute(sql)

