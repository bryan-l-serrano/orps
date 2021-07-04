from flask import Flask, request, jsonify, Response
import createFunction
import readFunctions
#import updateFunctions
#import deleteFunctions
import json

app = Flask(__name__)



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

@app.route('/orps/playerStats', methods =['GET'])
def getAllPlayerStats():
    try:
        playerData = readFunctions.getAllPlayerStats()
    except:
        return Response(json.dumps({"STATUS": "ERROR", "message": "something went wrong with the request"}), 400, mimetype='application/json')
    else:
        return Response(json.dumps(playerData), 200, mimetype='application/json')



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





if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5050)