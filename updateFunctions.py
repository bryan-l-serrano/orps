#!/usr/bin/python
import sqlite3
import string
import os

def updatePlayerPassword(playerId, newPassword):
    conn = sqlite3.connect('/orps/orps.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("UPDATE PLAYER SET password = ? WHERE PlayerID = ?", (newPassword,playerId,))
    cursor.execute("SELECT * FROM PLAYER WHERE id = ?", (playerId,))
    returnData = [dict(row) for row in cursor.fetchall()]
    conn.commit()
    conn.close()
    return returnData

def updateThrown(rock, paper, scissors, playerID):
    print(" in updatefunctions: rock: " + str(rock) + "\npaper: " + str(paper) + "\nscissors: " + str(scissors))
    print(playerID)
    conn = sqlite3.connect('/orps/orps.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("UPDATE PLAYER_STATS SET rocksThrown = ?, papersThrow = ?, scissorsThrown = ? WHERE playerID = ?", (rock, paper, scissors, playerID,))
    print("first sql command executed")
    cursor.execute("SELECT * FROM PLAYER_STATS WHERE playerID = ?", (playerID,))
    returnData = [dict(row) for row in cursor.fetchall()]
    conn.commit()
    conn.close()
    return returnData
