#!/usr/bin/python
import sqlite3
import os

conn = sqlite3.connect('/orps/orps.db')

print('opened database')

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS PLAYER_STATS")

sqlCommand = '''CREATE TABLE PLAYER_STATS(
playerID CHAR(20) PRIMARY KEY NOT NULL,
eloRating INT NOT NULL,
rocksThrown INT NOT NULL,
papersThrow INT NOT NULL,
scissorsThrown INT NOT NULL,
gamesPlayed INT NOT NULL,
gamesWon INT NOT NULL
)'''

cursor.execute(sqlCommand)

conn.commit()

print('created table')

conn.close()