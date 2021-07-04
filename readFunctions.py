#!/usr/bin/python
import sqlite3
import string
import os


def getPlayerByID(idval):
    conn = sqlite3.connect('/orps/orps.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PLAYER WHERE playerID = ?", (idval,))
    returnData = [dict(row) for row in cursor.fetchall()]
    conn.commit()
    conn.close()
    return returnData

def getPlayerByUsername(username):
    conn = sqlite3.connect('/orps/orps.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PLAYER WHERE username = ?", (username,))
    returnData = [dict(row) for row in cursor.fetchall()]
    conn.commit()
    conn.close()
    return returnData

def getAllPlayers():
    conn = sqlite3.connect('/orps/orps.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PLAYER")
    returnData = [dict(row) for row in cursor.fetchall()]
    conn.commit()
    conn.close()
    return returnData

def getAllPlayerStats():
    conn = sqlite3.connect('/orps/orps.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PLAYER_STATS")
    returnData = [dict(row) for row in cursor.fetchall()]
    conn.commit()
    conn.close()
    return returnData

def getPlayerStatsbyID(idval):
    conn = sqlite3.connect('/orps/orps.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PLAYER_STATS WHERE playerID = ?", (idval,))
    returnData = [dict(row) for row in cursor.fetchall()]
    conn.commit()
    conn.close()
    return returnData

def getGamebyID(idval):
    conn = sqlite3.connect('/orps/orps.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM GAME WHERE gameID = ?", (idval,))
    returnData = [dict(row) for row in cursor.fetchall()]
    conn.commit()
    conn.close()
    return returnData

def getGamesbyPlayerID(idval):
    conn = sqlite3.connect('/orps/orps.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM GAME WHERE player1ID = ? OR player2ID = ?", (idval,idval,))
    returnData = [dict(row) for row in cursor.fetchall()]
    conn.commit()
    conn.close()
    return returnData

def getGamesbyPlayerWonID(idval):
    conn = sqlite3.connect('/orps/orps.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM GAME WHERE winPlayerID = ?", (idval,))
    returnData = [dict(row) for row in cursor.fetchall()]
    conn.commit()
    conn.close()
    return returnData