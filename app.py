from flask import Flask, request, jsonify, Response
import createFunction
import readFunctions
import updateFunctions
#import deleteFunctions
import json
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

playerQueue = []


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
    try:
        returnData = readFunctions.getPlayerStatsbyID(playerID)
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "something went wrong with the request"}), 400, mimetype='application/json')
    else:
        timeEntered = time.time()
        stats = returnData[0]
        toAddToQueue = {"playerID": playerID, "eloRating": stats["eloRating"], "timeEnteredQueue":timeEntered}
        playerQueue.append(toAddToQueue)
        

        if len(playerQueue)>= 2:
            playerData = {}
            eloDifference = 999999
            closestRatedPlayerInQueue = 0
            firstPlayer = playerQueue[0]
            for x in range(1, len(playerQueue)):
                if abs(firstPlayer["eloRating"] - playerQueue[x]["eloRating"]) < eloDifference:
                    eloDifference = abs(firstPlayer["eloRating"] - playerQueue[x]["eloRating"])
                    closestRatedPlayerInQueue = x
                    if eloDifference == 0:
                        playerData = {"player1ID":firstPlayer["playerID"], "player2ID":playerQueue[x]["playerID"]}
                        print(playerData)
            if not bool(playerData):
                playerData = {"player1ID":firstPlayer["playerID"], "player2ID":playerQueue[closestRatedPlayerInQueue]["playerID"]}
                print(playerData)
            try:
                createFunction.createGame(playerData)
                del playerQueue[closestRatedPlayerInQueue]
                del playerQueue[0]
            except:
                print("Not able to create game")
        print(playerQueue)



        return Response(json.dumps({"STATUS":"SUCESS","message":"Player Added to Queue","timeStamp":timeEntered}), 200, mimetype='application/json')


##################################################################################
#################### UPDATE ####################################


@app.route('/orps/throw', methods=['POST'])
def updateThrown():
    if not request.json:
        return json.dumps({"STATUS": "ERROR", "message": "No request sent"}), 400
    playerData = request.get_json()
    playerID = playerData["playerID"]
    handThrown = playerData["thrown"]
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

    print("rock: " + str(rock) + "\npaper: " + str(paper) + "\nscissors: " + str(scissors))
    try:
        updateThrown = updateFunctions.updateThrown(rock, paper, scissors, playerID)
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "something went wrong with the request"}), 400, mimetype='application/json')
    else:
        stats = updateThrown[0]
        del stats['playerID']
        return Response(json.dumps({"STATUS":"SUCESS","playerData":stats}), 200, mimetype='application/json')


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
