#!/usr/bin/python
import sqlite3
import os

conn = sqlite3.connect('/orps/orps.db')

print('opened database')

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS GAME")

sqlCommand = '''CREATE TABLE GAME(
gameID CHAR(20) PRIMARY KEY NOT NULL,
player1ID CHAR(20) NOT NULL,
player2ID CHAR(20) NOT NULL,
winPlayerID CHAR(20) NOT NULL,
status CHAR(20) NOT NULL,
player1Throw CHAR(15) NOT NULL,
player2Throw CHAR(15) NOT NULL,
round INT NOT NULL,
player1WinCount INT NOT NULL,
player2WinCount INT NOT NULL
)'''

cursor.execute(sqlCommand)

conn.commit()

print('created table')

conn.close()