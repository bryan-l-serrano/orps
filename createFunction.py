#!/usr/bin/python
import sqlite3
import random
import string
import os
import readFunctions
import otp

def createID():
    return ''.join(random.sample(string.ascii_letters + string.digits, k=20))

def createPlayer(playerData):
    pID = createID()
    key = open("/orps/key.txt", "r").readline()
    data = (pID, playerData["userName"].lower(), str(otp.encryptStrings(playerData['password'], key)))
    #print(data)
    conn = sqlite3.connect('/orps/orps.db')
    #print('connected to db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO PLAYER VALUES (?,?,?)", (data),)
    psdat = (pID, 1100, 0, 0, 0, 0, 0)
    cursor.execute("INSERT INTO PLAYER_STATS VALUES (?,?,?,?,?,?,?)", (psdat),)
    #print('playerStats created')
    conn.commit()

    #print('closing connection to db')
    conn.close()

    return True

def createGame(player1ID, player2ID):
    gID = createID()
    data = (gID, player1ID, player2ID, "", "CREATED", "", "", 1, 0, 0)
    #print(data)
    conn = sqlite3.connect('/orps/orps.db')
    #print('connected to db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO GAME VALUES (?,?,?,?,?,?,?,?,?,?)", data)
    #print('game created')
    conn.commit()
    #print('closing connection to db')
    conn.close()
    returnGame = readFunctions.getGamebyID(gID)
    return returnGame