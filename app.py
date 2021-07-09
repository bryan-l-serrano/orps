from flask import Flask, request, jsonify, Response
import createFunction
import readFunctions
import updateFunctions
#import deleteFunctions
import json
from flask_cors import CORS
import time
import threading

app = Flask(__name__)
CORS(app)
playerQueue = []
gameList = []

##################################################
######### HELPER FUNCTIONS########################

def set_interval(func, sec, exitFunction):
    def func_wrapper():
        if not exitFunction():
            set_interval(func, sec, exitFunction)
            func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def createGameCheckerFunction(playerID,timesAttempted):
    try:
        gameData = readFunctions.getGamebyPlayerIDAndStatus("playerID")
    except:
        print('no game available')
    else:
        if bool(gameData):
            gameFound[0] = True
            #gameResponse.append(Response(json.dumps({"STATUS": "SUCCESS", "gameID":gameData[0]['gameID'], "player1ID":gameData[0]['player1ID'], "player2ID":gameData[0]['player2ID']}), 200, mimetype='application/json'))
            return Response(json.dumps({"STATUS": "SUCCESS", "gameID":gameData[0]['gameID'], "player1ID":gameData[0]['player1ID'], "player2ID":gameData[0]['player2ID']}), 200, mimetype='application/json')
        if len(playerQueue)>= 2:
            checkqueue = [i for i in playerQueue if not (i['playerID'] == playerID)]
            eloDifference = 60 + 20 * timesAttempted
            for x in range(1, len(checkqueue)):
                if abs(stats['eloRating'] - checkqueue[x]['eloRating']) <= eloDifference:
                    try:
                        newGame = createFunction.createGame(playerID, checkqueue[i]['playerID'])
                    except:
                        #gameResponse.append(Response(json.dumps({"STATUS": "ERROR", "message": "cannot create game"}), 400, mimetype='application/json'))
                        return Response(json.dumps({"STATUS": "ERROR", "message": "cannot create game"}), 400, mimetype='application/json')
                    else:
                        playerQueue = [i for i in playerQueue if not (i['playerID'] == playerID or i['playerID'] == checkqueue[x]['playerID'])]
                        #gameResponse.append(Response(json.dumps({"STATUS": "SUCCESS", "gameID": newGame[0]['gameID'], "player1ID": newGame[0]["player1ID"], "player2ID":newGame[0]["player2ID"]}), 200, mimetype='application/json'))
                        return Response(json.dumps({"STATUS": "SUCCESS", "gameID": newGame[0]['gameID'], "player1ID": newGame[0]["player1ID"], "player2ID":newGame[0]["player2ID"]}), 200, mimetype='application/json')      
            timesAttempted[0] += 1
            print("playerID: " + str(playerID) + " times attempted: " + str(timesAttempted)[0])
            if timesAttempted[0] == 7:
                #gameResponse.append(Response(json.dumps({"STATUS": "ERROR", "message": "no players found"}), 400, mimetype='application/json'))
                return Response(json.dumps({"STATUS": "ERROR", "message": "no players found"}), 400, mimetype='application/json')

def exitFunction(times):
    if times[0] == 6:
        return true

#######################################
#CREATE
@app.route('/orps/newPlayer', methods=['POST'])
def createPlayer():
    if not request.json:
        return json.dumps({"STATUS": "ERROR", "message": "No request sent"}), 400
    playerData = request.get_json()
    try:
        createFunction.createPlayer(playerData)
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "something went wrong with the request"}), 400, mimetype='application/json')
    else:
        return Response(json.dumps({"STATUS": "SUCCESS", "message": "player successfully created"}), 201, mimetype='application/json')

@app.route('/orps/createGame', methods=['POST'])
def createGame():
    if not request.json:
        return json.dumps({"STATUS": "ERROR", "message": "No request sent"}), 400
    playerData = request.get_json()
    try:
        newGame = createFunction.createGame(playerData)
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "something went wrong with the request"}), 400, mimetype='application/json')
    else:
        return Response(json.dumps({"STATUS": "SUCCESS", "message": "game successfully created", "gameData":newGame}), 200, mimetype='application/json')

###################################################
######## READ ###################################


@app.route('/orps/player', methods =['GET'])
def getAllPlayers():
    try:
        playerData = readFunctions.getAllPlayers()
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "something went wrong with the request"}), 400, mimetype='application/json')
    else:
        return Response(json.dumps(playerData), 200, mimetype='application/json')

@app.route('/orps/game', methods = ['GET'])
def getAllGames():
    try:
        gameData = readFunctions.getAllGames()
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "something went wrong with the request"}), 400, mimetype='application/json')
    else:
        return Response(json.dumps(gameData), 200, mimetype='application/json')

@app.route('/orps/playerStats', methods =['GET'])
def getAllPlayerStats():
    try:
        playerData = readFunctions.getAllPlayerStats()
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "something went wrong with the request"}), 400, mimetype='application/json')
    else:
        return Response(json.dumps(playerData), 200, mimetype='application/json')

@app.route('/orps/playerStat', methods = ['POST'])
def getPlayerStats():
    if not request.json:
        return json.dumps({"STATUS": "ERROR", "message": "No request sent"}), 400
    playerData = request.get_json()
    playerID = playerData["playerID"]
    try:
        returnData = readFunctions.getPlayerStatsbyID(playerID)
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "something went wrong with the request"}), 400, mimetype='application/json')
    else:
        stats = returnData[0]
        del stats['playerID']
        return Response(json.dumps({"STATUS":"SUCESS","playerData":stats}), 200, mimetype='application/json')

################################################
############## LOGIN ###########################

@app.route('/orps/login', methods=['POST'])
def login():
    if not request.json:
        return json.dumps({"STATUS": "ERROR", "message": "No request sent"}), 400
    playerData = request.get_json()
    try:
        getPlayer = readFunctions.getPlayerByUsername(playerData["username"])
        if playerData["password"] == getPlayer[0]["password"]:
            return Response(json.dumps({"STATUS":"SUCCESS","playerID":(getPlayer[0])["playerID"]}), 200, mimetype='application/json')
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "something went wrong with the request"}), 400, mimetype='application/json')
    else:
        return Response(json.dumps({"STATUS": "ERROR", "message": "The username or password doesn't match"}), 400, mimetype='application/json')


#################################################
############# QUEUE #############################

@app.route('/orps/queue', methods=['POST'])
def addToQueue():
    if not request.json:
        return json.dumps({"STATUS": "ERROR", "message": "No request sent"}), 400
    playerData = request.get_json()
    playerID = playerData["playerID"]
    gameResponse = []
    gameFound = [False]
    timesAttempted = [0]
    global playerQueue
    for x in playerQueue:
        if x['playerID'] == playerID:
            playerQueue = [i for i in playerQueue if not (i['playerID'] == playerID)]
    try:
        returnData = readFunctions.getPlayerStatsbyID(playerID)
        timeEntered = time.time()
        stats = returnData[0]
        toAddToQueue = {"playerID": playerID, "eloRating": stats["eloRating"], "timeEnteredQueue":timeEntered}
        playerQueue.append(toAddToQueue)
        #print(playerQueue)
        return Response(json.dumps({"STATUS": "SUCCESS", "message": "Player added to Queue"}), 200, mimetype='application/json')
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "Issue adding player to queue"}), 400, mimetype='application/json')
    
    # set_interval(createGameCheckerFunction(playerID, gameFound, timesAttempted), 10, exitFunction(timesAttempted), gameResponse)

    # while len(gameResponse) < 1:
        

    return gameResponse[0]

        # if len(playerQueue)>= 2:
        #     playerData = {}
        #     eloDifference = 999999
        #     closestRatedPlayerInQueue = 0
        #     firstPlayer = playerQueue[0]
        #     for x in range(1, len(playerQueue)):
        #         if abs(firstPlayer["eloRating"] - playerQueue[x]["eloRating"]) < eloDifference:
        #             eloDifference = abs(firstPlayer["eloRating"] - playerQueue[x]["eloRating"])
        #             closestRatedPlayerInQueue = x
        #             if eloDifference == 0:
        #                 playerData = {"player1ID":firstPlayer["playerID"], "player2ID":playerQueue[x]["playerID"]}
        #                 print(playerData)
        #     if not bool(playerData):
        #         playerData = {"player1ID":firstPlayer["playerID"], "player2ID":playerQueue[closestRatedPlayerInQueue]["playerID"]}
        #         print(playerData)
        #     try:
        #         createFunction.createGame(playerData)
        #         del playerQueue[closestRatedPlayerInQueue]
        #         del playerQueue[0]
        #     except:
        #         print("Not able to create game")
        # print(playerQueue)

@app.route('/orps/check', methods=['POST'])
def addToGame():
    if not request.json:
        return json.dumps({"STATUS": "ERROR", "message": "No request sent"}), 400
    playerData = request.get_json()
    playerID = playerData["playerID"]
    timesAttempted = playerData['requestNumber']
    global playerQueue
    global gameList
    gameData = False
    if timesAttempted < 6:
        stats = readFunctions.getPlayerStatsbyID(playerID)
        try:
            gameData = readFunctions.getGamebyPlayerIDAndStatus(playerID)
        except:
            print('no game available')
        if bool(gameData):
            #gameResponse.append(Response(json.dumps({"STATUS": "SUCCESS", "gameID":gameData[0]['gameID'], "player1ID":gameData[0]['player1ID'], "player2ID":gameData[0]['player2ID']}), 200, mimetype='application/json'))
            return Response(json.dumps({"STATUS": "SUCCESS", "gameID":gameData[0]['gameID'], "player1ID":gameData[0]['player1ID'], "player2ID":gameData[0]['player2ID']}), 200, mimetype='application/json')
        if len(playerQueue)>= 2:
            checkqueue = [i for i in playerQueue if not (i['playerID'] == playerID)]
            #print(checkqueue)
            eloDifference = 40 + 20 * timesAttempted
            for x in range(0, len(checkqueue)):
                if abs(int(stats[0]['eloRating']) - int(checkqueue[x]['eloRating'])) <= eloDifference:
                    try:
                        newGame = createFunction.createGame(playerID, checkqueue[x]['playerID'])
                    except:
                        #gameResponse.append(Response(json.dumps({"STATUS": "ERROR", "message": "cannot create game"}), 400, mimetype='application/json'))
                        return Response(json.dumps({"STATUS": "ERROR", "message": "cannot create game"}), 400, mimetype='application/json')
                    else:
                        playerQueue = [i for i in playerQueue if not (i['playerID'] == playerID or i['playerID'] == checkqueue[x]['playerID'])]
                        #gameResponse.append(Response(json.dumps({"STATUS": "SUCCESS", "gameID": newGame[0]['gameID'], "player1ID": newGame[0]["player1ID"], "player2ID":newGame[0]["player2ID"]}), 200, mimetype='application/json'))
                        #print(newGame[0])
                        print(playerQueue)
                        gameList.append({"gameID":newGame[0]['gameID'], "player1ID":gameData[0]['player1ID'], "player2ID":gameData[0]['player2ID'], "player1thrown":"", "player2Thrown":"", "player1Wins":0, "player2Wins":0})
                        return Response(json.dumps({"STATUS": "SUCCESS", "gameID": newGame[0]['gameID'], "player1ID": newGame[0]["player1ID"], "player2ID":newGame[0]["player2ID"]}), 200, mimetype='application/json')      
            
            return Response(json.dumps({"STATUS": "SUCCESS", "message": "No game found"}), 200, mimetype='application/json')
        else:
            return Response(json.dumps({"STATUS": "SUCCESS", "message": "Not Enough Players"}), 200, mimetype='application/json')
    else:
        try:
            gameData = readFunctions.getGamebyPlayerIDAndStatus("playerID")
        except:
            print('no game available')
        else:
            if bool(gameData):
                #gameResponse.append(Response(json.dumps({"STATUS": "SUCCESS", "gameID":gameData[0]['gameID'], "player1ID":gameData[0]['player1ID'], "player2ID":gameData[0]['player2ID']}), 200, mimetype='application/json'))
                return Response(json.dumps({"STATUS": "SUCCESS", "gameID":gameData[0]['gameID'], "player1ID":gameData[0]['player1ID'], "player2ID":gameData[0]['player2ID']}), 200, mimetype='application/json')
            playerQueue = [i for i in playerQueue if not (i['playerID'] == playerID)]
            return Response(json.dumps({"STATUS": "SUCCESS", "message": "Could not Join Game; player removed from queue"}), 200, mimetype='application/json')

##################################################################################
#################### UPDATE ####################################


@app.route('/orps/throw', methods=['POST'])
def updateThrown():
    if not request.json:
        return json.dumps({"STATUS": "ERROR", "message": "No request sent"}), 400
    playerData = request.get_json()
    playerID = playerData["playerID"]
    handThrown = playerData["thrown"]
    gameID = playerData["gameID"]
    try:
        playerStats = readFunctions.getPlayerStatsbyID(playerID)
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "playerID invalid"}), 400, mimetype='application/json')
    rock = int(playerStats[0]["rocksThrown"])
    paper = int(playerStats[0]["papersThrow"])
    scissors = int(playerStats[0]["scissorsThrown"])
    if handThrown == "rock":
        rock += 1
    elif handThrown == "paper":
        paper += 1
    elif handThrown == "scissors":
        scissors += 1
    else:
        return Response(json.dumps({"STATUS": "ERROR", "message": "What did you just send?"}), 400, mimetype='application/json')

    #print("rock: " + str(rock) + "\npaper: " + str(paper) + "\nscissors: " + str(scissors))
    try:
        updateThrown = updateFunctions.updateThrown(rock, paper, scissors, playerID)
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "something went wrong with the request"}), 400, mimetype='application/json')
    else:
        stats = updateThrown[0]
        del stats['playerID']
    


@app.route('/orps/updateStats', methods = ['POST'])
def updateStats():
    if not request.json:
        return json.dumps({"STATUS": "ERROR", "message": "No request sent"}), 400
    playerData = request.get_json()
    player1ID = playerData['player1ID']
    player2ID = playerData['player2ID']
    playerWonID = playerData['winPlayerID']
    gameID = playerData['gameID']
    print(player1ID)
    try:
        player1Stats = readFunctions.getPlayerStatsbyID(player1ID)
        print(player1Stats)
        player2Stats = readFunctions.getPlayerStatsbyID(player2ID)
        print(player2Stats)
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "Invalid ID's"}), 400, mimetype='application/json')

    try:
        updateFunctions.updatePlayerStats(player1Stats[0], player2Stats[0], playerWonID)
        print("player 1 updated")
        updateFunctions.updatePlayerStats(player2Stats[0], player1Stats[0], playerWonID)
        print("player 2 updated")
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "unable to update player"}), 400, mimetype='application/json')
    
    try:
        updateFunctions.updateGame(gameID, playerWonID)
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "unable to update game"}), 400, mimetype='application/json')
    else:
        return Response(json.dumps({"STATUS":"SUCCESS", "message":"Players and Game Successfully Updated"}), 200, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5050)
