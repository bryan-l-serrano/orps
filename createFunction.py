#!/usr/bin/python
import sqlite3
import random
import string
import os

def createID():
    return ''.join(random.sample(string.ascii_letters + string.digits, k=20))

def createPlayer(playerData):
    pID = createID()
    data = (pID, playerData["userName"], playerData['password'])
    print(data)
    conn = sqlite3.connect('/orps/orps.db')
    print('connected to db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO PLAYER VALUES (?,?,?)", data)
    print('player created')
    psdat = (pID, 1000, 0, 0, 0, 0, 0)
    cursor.execute("INSERT INTO PLAYER_STATS VALUES (?,?,?,?,?,?,?)", psdat)
    print('playerStats created')
    conn.commit()

    print('closing connection to db')
    conn.close()

    return True

def createGame(gameData):
    gID = createID()
    data = (gID, gameData["player1ID"], gameData['player2ID'], "")
    print(data)
    conn = sqlite3.connect('/orps/orps.db')
    print('connected to db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO GAME VALUES (?,?,?,?)", data)
    print('game created')
    conn.commit()

    print('closing connection to db')
    conn.close()

    return True