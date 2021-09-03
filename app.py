from flask import Flask, request, jsonify, Response
import createFunction
import readFunctions
import updateFunctions
#import deleteFunctions
import json
from flask_cors import CORS
import time
import threading
import random
import string

app = Flask(__name__)
CORS(app)
playerQueue = []
gameList = []

##################################################
######### HELPER FUNCTIONS########################

def createID():
    return ''.join(random.sample(string.ascii_letters + string.digits, k=20))

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

def rpsComare(p1, p2, p1ID, p2ID):
    if(p1 == p2):
        return "draw"
    elif(p1 == "nothing"):
        return p2ID
    elif(p2 == "nothing"):
        return p1ID
    elif(p1 == "rock" and p2 == "paper"):
        return p2ID
    elif(p1 == "rock" and p2 == "scissors"):
        return p1ID
    elif(p1 == "paper" and p2 == "rock"):
        return p1ID
    elif(p1 == "paper" and p2 == "scissors"):
        return p2ID
    elif(p1 == "scissors" and p2 == "rock"):
        return p2ID
    elif(p1 == "scissors" and p2 == "paper"):
        return p1ID
    

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
        for games in gameList:
            if games['player1ID'] == playerID or games['player2ID'] == playerID:
                return Response(json.dumps({"STATUS": "SUCCESS", "gameID":games['gameID'], "player1ID":games['player1ID'], "player2ID":games['player2ID']}), 200, mimetype='application/json')
        if len(playerQueue)>= 2:
            checkqueue = [i for i in playerQueue if not (i['playerID'] == playerID)]
            eloDifference = 40 + 20 * timesAttempted
            for x in range(0, len(checkqueue)):
                if abs(int(stats[0]['eloRating']) - int(checkqueue[x]['eloRating'])) <= eloDifference:
                    newGameID = createID()
                    gameList.append({"gameID":newGameID, "player1ID":playerID, "player2ID":checkqueue[x]['playerID'], "player1Thrown":"", "player2Thrown":"", "player1Wins":0, "player2Wins":0, "result":"", "finalGameStatus":"", "player1Check":False, "player2Check":False})
                    playerQueue = [i for i in playerQueue if not (i['playerID'] == playerID or i['playerID'] == checkqueue[x]['playerID'])]
                    #print(playerQueue)
                    return Response(json.dumps({"STATUS": "SUCCESS", "gameID": newGameID, "player1ID": playerID, "player2ID":checkqueue[x]['playerID']}), 200, mimetype='application/json')            
            return Response(json.dumps({"STATUS": "SUCCESS", "message": "No game found"}), 200, mimetype='application/json')
        else:
            return Response(json.dumps({"STATUS": "SUCCESS", "message": "Not Enough Players"}), 200, mimetype='application/json')
    else:
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
    player1ID = None
    player2ID = None
    global gameList

    for games in gameList:
        if games['gameID'] == gameID:
            if games['player1ID'] == playerID:
                player1ID = playerID
            else:
                player2ID = playerID
    try:
        playerStats = readFunctions.getPlayerStatsbyID(playerID)
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "playerID invalid"}), 400, mimetype='application/json')
    rock = int(playerStats[0]["rocksThrown"])
    paper = int(playerStats[0]["papersThrow"])
    scissors = int(playerStats[0]["scissorsThrown"])
    if handThrown == "rock":
        rock += 1
        for games in gameList:
            if games['gameID'] == gameID:
                if(player1ID):
                    games['player1Thrown'] = 'rock'
                else:
                    games['player2Thrown'] = 'rock'
    elif handThrown == "paper":
        paper += 1
        for games in gameList:
            if games['gameID'] == gameID:
                if(player1ID):
                    games['player1Thrown'] = 'paper'
                else:
                    games['player2Thrown'] = 'paper'
    elif handThrown == "scissors":
        scissors += 1
        for games in gameList:
            if games['gameID'] == gameID:
                if(player1ID):
                    games['player1Thrown'] = 'scissors'
                else:
                    games['player2Thrown'] = 'scissors'
    elif handThrown == "nothing":
        for games in gameList:
            if games['gameID'] == gameID:
                if(player1ID):
                    games['player1Thrown'] = 'nothing'
                else:
                    games['player2Thrown'] = 'nothing'
    else:
        return Response(json.dumps({"STATUS": "ERROR", "message": "What did you just send?"}), 400, mimetype='application/json')
    #print(gameList)
    #print("rock: " + str(rock) + "\npaper: " + str(paper) + "\nscissors: " + str(scissors))
    try:
        updateThrown = updateFunctions.updateThrown(rock, paper, scissors, playerID)
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "something went wrong with the request"}), 400, mimetype='application/json')
    else:
        for games in gameList:
            if games['gameID'] == gameID:
                if(games['player1Thrown'] != "" and games['player2Thrown'] != ""):
                    result = rpsComare(games['player1Thrown'], games['player2Thrown'], games["player1ID"], games['player2ID'])
                    if result == "draw":
                        games['result'] = "draw"
                        games['player1Thrown'] = ""
                        games['player2Thrown'] = ""
                    elif result == games['player1ID']:
                        games['player1Wins'] += 1
                        games['result'] = result
                        games['player1Thrown'] = ""
                        games['player2Thrown'] = ""
                    elif result == games['player2ID']:
                        games['player2Wins'] += 1
                        games['result'] = result
                        games['player1Thrown'] = ""
                        games['player2Thrown'] = ""
                    else:
                        return Response(json.dumps({"STATUS": "ERROR", "message": "you what"}), 400, mimetype='application/json')
                elif (games['player1Thrown'] != "" or games['player2Thrown'] != ""):
                    games['results'] = ""
                if (games['player1Wins'] == 2):
                    games['finalGameStatus'] = games['player1ID']
                if (games['player2Wins'] == 2):
                    games['finalGameStatus'] = games['player2ID']
        #print(gameList)

        return Response(json.dumps({"STATUS": "SUCCESS", "message": "you did it!"}), 200, mimetype='application/json')

    
@app.route('/orps/checkRound', methods = ['POST'])
def checkRound():
    if not request.json:
        return json.dumps({"STATUS": "ERROR", "message": "No request sent"}), 400
    playerData = request.get_json()
    gameID = playerData["gameID"]
    playerID = playerData['playerID']
    player1ID = None
    player2ID = None
    global gameList

    for games in gameList:
        if games['gameID'] == gameID:
            if games['player1ID'] == playerID:
                player1ID = playerID
            else:
                player2ID = playerID


    for games in gameList:
        if games['gameID'] == gameID:
            #print(games)
            if games['finalGameStatus']:
                if(player1ID):
                    games['player1Check'] = True
                else:
                    games['player2Check'] = True
            return Response(json.dumps({"STATUS": "SUCCESS", "gameData": games}), 200, mimetype='application/json')
    return Response(json.dumps({"STATUS": "ERROR", "message":"gameID was not found -> deleted before accessing"}), 400, mimetype='application/json')


@app.route('/orps/updateStats', methods = ['POST'])
def updateStats():
    global gameList
    if not request.json:
        return json.dumps({"STATUS": "ERROR", "message": "No request sent"}), 400
    playerData = request.get_json()
    player1ID = playerData['player1ID']
    player2ID = playerData['player2ID']
    playerWonID = playerData['playerWonID']
    gameID = playerData['gameID']
    #print(player1ID)
    try:
        player1Stats = readFunctions.getPlayerStatsbyID(player1ID)
        print(player1Stats)
        player2Stats = readFunctions.getPlayerStatsbyID(player2ID)
        print(player2Stats)
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "Invalid ID's"}), 400, mimetype='application/json')

    try:
        print("atempting to update")
        updateFunctions.updatePlayerStats(player1Stats[0], player2Stats[0], playerWonID)
        print("player 1 updated")
        updateFunctions.updatePlayerStats(player2Stats[0], player1Stats[0], playerWonID)
        print("player 2 updated")
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "unable to update player"}), 400, mimetype='application/json')
    print(gameID)
    print(gameList)
    gameList = [ i for i in gameList if not (i['gameID'] == gameID)]
    print(gameList)
    return Response(json.dumps({"STATUS":"SUCCESS", "message":"Players and Game Successfully Updated"}), 200, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5050)
