#!/usr/bin/python
import sqlite3
import string
import os
import readFunctions

k = 32

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


def updatePlayerStats(player1Stats, player2Stats, playerWinID):
    conn = sqlite3.connect('/orps/orps.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if player1Stats["playerID"] == playerWinID:
        win = 1
        playerWon = True
    else:
        win = 0
        playerWon = False
    curPlayerElo = player1Stats['eloRating']
    opponenetElo = player2Stats['eloRating']
    curEx = float(1 / (1 + 10**((opponenetElo - curPlayerElo)/400)))
    newElo = int(curPlayerElo + k*(win - curEx))

    if playerWon:  
        cursor.execute("UPDATE PLAYER_STATS SET gamesPlayed = ?, gamesWon = ?, eloRating = ? WHERE playerID = ?", (player1Stats["gamesPlayed"] + 1, player1Stats["gamesWon"] + 1, int(newElo), player1Stats["playerID"],))
    else:
        cursor.execute("UPDATE PLAYER_STATS SET gamesPlayed = ?, eloRating = ? WHERE playerID = ?", (player1Stats["gamesPlayed"] + 1, int(newElo), player1Stats["playerID"],))
    cursor.execute("SELECT * FROM PLAYER_STATS WHERE playerID = ?", (player1Stats['playerID'],))
    returnData = [dict(row) for row in cursor.fetchall()]
    conn.commit()
    conn.close()
    return returnData


def updateGame(gameID, playerWinID):
    conn = sqlite3.connect('/orps/orps.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    print("do i get this far")
    cursor.execute("UPDATE GAME SET winPlayerID = ? WHERE gameID = ?", (playerWinID, gameID,))
    print("how about here?")
    conn.commit()
    conn.close()