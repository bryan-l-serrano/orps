#!/usr/bin/python
import sqlite3
import os

conn = sqlite3.connect('/orps/orps.db')

print('opened database')

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS PLAYER")

sqlCommand = '''CREATE TABLE PLAYER(
playerID CHAR(20) PRIMARY KEY NOT NULL,
username CHAR(30) UNIQUE NOT NULL,
password CHAR(30) NOT NULL
)'''

cursor.execute(sqlCommand)

conn.commit()

print('created table')

conn.close()